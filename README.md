# llm-tools-jira

[![PyPI](https://img.shields.io/pypi/v/llm-tools-jira.svg)](https://pypi.org/project/llm-tools-jira/)
[![Changelog](https://img.shields.io/github/v/release/guspix/llm-tools-jira?include_prereleases&label=changelog)](https://github.com/guspix/llm-tools-jira/releases)
[![Tests](https://github.com/guspix/llm-tools-jira/actions/workflows/test.yml/badge.svg)](https://github.com/guspix/llm-tools-jira/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/guspix/llm-tools-jira/blob/main/LICENSE)

Manage Jira issues using LLMs

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-tools-jira
```
## Usage

To use this with the [LLM command-line tool](https://llm.datasette.io/en/stable/usage.html):

```bash
llm --tool create_issue "Example prompt goes here" --tools-debug
```

With the [LLM Python API](https://llm.datasette.io/en/stable/python-api.html):

```python
import llm
from llm_tools_jira import create_issue

model = llm.get_model("gpt-4.1-mini")

result = model.chain(
    "Example prompt goes here",
    tools=[create_issue]
).text()
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-tools-jira
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
