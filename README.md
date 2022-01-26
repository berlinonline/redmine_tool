# Redmine Tool

A collection of python scripts to do stuff with the [Redmine API](https://www.redmine.org/projects/redmine/wiki/Rest_api).

## Requirements

- Python 3
- Environment variables:
    - REDMINE_URL
    - REDMINE_API_KEY

## Installation

Create a virtual environment:

```shell
% python -m venv redmine_tool_venv
```

Activate virtual environment:

```shell
% . redmine_tool_venv/bin/activate
(redmine_tool_venv) %
```

Install dependencies:

```shell
(redmine_tool_venv) % pip install -r requirements.txt
```

### Tools

#### Issue Tree

You can run `issue_tree.py` to retrieve a tree of issues starting from a root issue.
The output is a JSON object that follows the structure outlined in https://www.redmine.org/projects/redmine/wiki/Rest_Issues, extended with an `children` attribute which contains an array of objects for each child.

```shell
usage: issue_tree.py [-h] -r ROOT

Retrieve a tree of issues given a root issue id.

optional arguments:
  -h, --help            show this help message and exit
  -r ROOT, --root ROOT  The id of the root issue.
```

For example:

```shell
(redmine_tool_venv) % python issue_tree.py -r 37446
INFO:root: Retrieving issue #37446 ...
INFO:root: Retrieving children for issue #37446 ...
INFO:root: Retrieving children for issue #46989 ...
INFO:root: Retrieving children for issue #46647 ...
...
INFO:root: Retrieving children for issue #36015 ...
INFO:root: Retrieving children for issue #36018 ...
INFO:root: Retrieving children for issue #36016 ...
```

```json
{
  "id": 37446,
  ...
  "children": [
    {
      "id": 46989,
      ...
      "children": [
        {
          "id": 46647,
          ...
        }
      ]
    }
  ]
}
```

### Tree-to-Dot

You can turn the output of `issue_tree.py` into SVG (via Graphviz's `.dot`) by running `tree2svg.py`. 

```shell
usage: tree2svg.py [-h] -i INPUT [-s START] [-m MAX_TITLE_LENGTH] [-d {TB,LR}] [-p PRUNE]

Convert a Redmine issues JSON tree to SVG. Either read through an input file, or pipe through STDIN. Output is to STDOUT.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        The path of a JSON file containing a Redmine issues tree, or '-' for STDIN.
  -s START, --start START
                        The issue id to use as the root of the output, if we only want to render a subtree. Default is the root of the input file.
  -m MAX_TITLE_LENGTH, --max_title_length MAX_TITLE_LENGTH
                        Truncate title length to this. Default is -1, meaning do not truncate.
  -d {TB,LR}, --direction {TB,LR}
                        Layout direction of the graph.
  -p PRUNE, --prune PRUNE
                        Comma-separated list of status ids. Issues with these status ids will be pruned.
```

## License

This material is copyright ©
[BerlinOnline Stadtportal GmbH & Co. KG]( https://www.berlinonline.net/).

All software in this repository is published under the [MIT License](LICENSE).
