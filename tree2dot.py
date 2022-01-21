import argparse
import json
import logging
import os
import pydot
import sys

REDMINE_URL = os.environ['REDMINE_URL']
ISSUE_BASE = os.path.join(REDMINE_URL, "issues")

def traverse_tree(node, graph, prune_status_ids):
    logging.info(f" stepping into #{node['id']} ({node['subject']}) ({node['status']})")
    my_node = pydot.Node(node['id'],
        shape="Mrecord",
        # style="rounded",
        label=f"{{{node['subject']}|#{node['id']}}}",
        href=os.path.join(REDMINE_URL, "issues", f"{node['id']}"))
    graph.add_node(my_node)
    for child in node.get('children', []):
        if not child['status']['id'] in prune_status_ids:
            traverse_tree(child, graph, prune_status_ids)
            graph.add_edge(pydot.Edge(node['id'], child['id'], color="blue"))

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Convert a Redmine issues JSON tree to a DOT file. Either read through an input file, or pipe through STDIN.")
parser.add_argument('-i', '--input', required=True,
                    help="The path of a JSON file containing a Redmine issues tree, or '-' for STDIN.")
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
    print("--input must be either a filepath or - for STDIN.")
    sys.exit(1)

graph = pydot.Dot(f"Issue Tree #{input_data['id']}", graph_type='graph')
traverse_tree(input_data, graph, prune_status_ids)

print(graph.to_string())

# logging.info(json.dumps(input_data, indent=2))


