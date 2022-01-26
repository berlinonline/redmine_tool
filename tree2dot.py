import argparse
import json
import logging
import os
import pydot
import sys

REDMINE_URL = os.environ['REDMINE_URL']
ISSUE_BASE = os.path.join(REDMINE_URL, "issues")

def font_wrap(text, color="black"):
    return f"<font color='{color}' face='Verdana, sans-serif'>{text}</font>"

def render_table(node, max_title_length=-1, always_render_progress=True):
    rows = []
    rows.append(render_title(node, max_title_length))
    rows.append(render_id(node))
    rows.append(render_category(node))
    if always_render_progress or node['done_ratio'] > 0:
        rows.append(render_progress(node))
    rows = [f"<tr>{row}</tr>" for row in rows]
    table_markup = f"{render_prefix(node)}f{''.join(rows)}{render_suffix(node)}"
    return table_markup

def render_prefix(node):
    markup = f"<table border='0' cellborder='0' cellpadding='3' cellspacing='1' bgcolor='black'>"
    return markup

def render_title(node, max_title_length=-1):
    title = node['subject']
    if len(title) > max_title_length:
        title = title[0:max_title_length-1]
        title = title + "…"
    markup = f"<td bgcolor='black' cellpadding='6'>{font_wrap(title, color='white')}</td>"
    return markup

def render_id(node):
    markup = f"<td bgcolor='white'>#{font_wrap(node['id'])}</td>"
    return markup

def render_category(node):
    category = node.get('category', {'name': '&lt;none&gt;'})
    category_text = f"<b>Kategorie:</b>&nbsp;{category['name']}"
    markup = f"<td bgcolor='white' align='left'>{font_wrap(category_text)}</td>"
    return markup

def render_progress(node):
    done_ratio = node['done_ratio']
    done_color = "#6da8ce" if done_ratio > 0 else "white"
    percent_text = f"{done_ratio}%"
    markup = f"<td bgcolor='white'><table border='0' cellborder='0' cellpadding='0'><tr><td width='100' border='1' bgcolor='{done_color};0.{done_ratio}:white'></td><td color='white' align='left'>&nbsp;{font_wrap(percent_text)}</td></tr></table></td>"
    return markup

def render_suffix(node):
    markup = f"</table>"
    return markup

def traverse_tree(node, graph, prune_status_ids, max_title_length=-1):
    logging.info(f" stepping into #{node['id']} ({node['subject']}) ({node['status']})")
    ticket_link = os.path.join(REDMINE_URL, "issues", f"{node['id']}")
    table_markup = render_table(node, max_title_length)
    my_node = pydot.Node(node['id'],
        shape="plaintext",
        fillcolor="white",
        style="filled",
        label=(f"<{table_markup}>"),
        href=ticket_link)
    graph.add_node(my_node)
    for child in node.get('children', []):
        if not child['status']['id'] in prune_status_ids:
            traverse_tree(child, graph, prune_status_ids, max_title_length)
            graph.add_edge(pydot.Edge(node['id'], child['id'], color="blue"))

def select_sub_tree(sub_tree_id, root_node):
    logging.info(f" looking for sub-tree in #{root_node['id']}")
    if root_node['id'] == sub_tree_id:
        return root_node
    for child in root_node.get('children', []):
        sub_tree = select_sub_tree(sub_tree_id, child)
        if sub_tree:
            return sub_tree
    return None

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Convert a Redmine issues JSON tree to a DOT file. Either read through an input file, or pipe through STDIN.")
parser.add_argument('-i', '--input', required=True,
                    help="The path of a JSON file containing a Redmine issues tree, or '-' for STDIN.")
parser.add_argument('-s', '--start',
                    type=int,
                    help="The issue id to use as the root of the output, if we only want to render a subtree. Default is the root of the input file.")
parser.add_argument('-m', '--max_title_length',
                    type=int, default=-1,
                    help="Truncate title length to this. Default is -1, meaning do not truncate.")
parser.add_argument('-d', '--direction',
                    default="TB",
                    choices=["TB","LR"],
                    help="Layout direction of the graph.")
parser.add_argument('-p', '--prune',
                    default="",
                    help="Comma-separated list of status ids. Issues with these status ids will be pruned.")
args = parser.parse_args()
prune_status_ids = [int(status_id) for status_id in args.prune.split(',')]

if os.path.isfile(args.input):
    input_file = open(args.input)
    input_data = json.load(input_file)
elif args.input == "-":
    input_data = json.loads(sys.stdin.read())
else:
    logging.error(" --input must be either a filepath or - for STDIN.")
    sys.exit(1)

if args.start:
    subtree_id = int(args.start)
    input_data = select_sub_tree(subtree_id, input_data)
    if not input_data:
        logging.error(f" Could not find subtree with node id #{subtree_id}.")
        sys.exit(1)

graph = pydot.Dot(f"Issue Tree #{input_data['id']}", graph_type='graph', rankdir=args.direction)
traverse_tree(input_data, graph, prune_status_ids, args.max_title_length)

print(graph.create_svg().decode("utf-8"))
