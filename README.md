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
(redmine_tool_venv) % python issue_tree.py -h
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

## License

This material is copyright ©
[BerlinOnline Stadtportal GmbH & Co. KG]( https://www.berlinonline.net/).

All software in this repository is published under the [MIT License](LICENSE).
