"""
Script to recursively retrieve a tree of issues, starting from the root.
Outputs result as JSON.

For documentation of Redmine-API (issues endpoint) see:
https://www.redmine.org/projects/redmine/wiki/Rest_Issues
"""

import argparse
import json
import logging
import os
import requests

logging.basicConfig(level=logging.INFO)

REDMINE_URL = os.environ['REDMINE_URL']
API_KEY = os.environ['REDMINE_API_KEY']
ISSUES_ENDPOINT = os.path.join(REDMINE_URL, 'issues.json')
HEADERS = {
    'X-Redmine-API-Key': API_KEY,
    'user-agent': 'bo_redmine_tool'
}

def retrieve_tree(issue_id):
    """Retrieve a tree of issues from Redmine, starting at `issue_id`."""
    logging.info(f" Retrieving issue #{issue_id} ...")

    params = {
        'issue_id': issue_id
    }
    response = requests.get(ISSUES_ENDPOINT, params=params, headers=HEADERS)
    data = json.loads(response.text)
    issue = data['issues'][0]
    issue['children'] = retrieve_children(issue_id)
    return issue

def retrieve_children(parent_id):
    """Retrieve all descendents of `parent_id` by recursively calling this function."""
    logging.info(f" Retrieving children for issue #{parent_id} ...")

    params = {
        'parent_id': parent_id,
        'status_id': '*'
    }
    response = requests.get(ISSUES_ENDPOINT, params=params, headers=HEADERS)
    data = json.loads(response.text)
    children = data['issues']
    for issue in children:
        issue['children'] = retrieve_children(issue['id'])

    return children

parser = argparse.ArgumentParser(description='Retrieve a tree of issues given a root issue id.')
parser.add_argument('-r', '--root', required=True,
                    help='The id of the root issue.')
args = parser.parse_args()
tree = retrieve_tree(args.root)
print(json.dumps(tree))
