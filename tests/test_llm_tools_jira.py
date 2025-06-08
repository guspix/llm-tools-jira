"""
Tests for llm_tools_jira.Jira toolbox.

Uses the `echo` model from the `llm-echo` plugin so we can drive
tool-calling deterministically, and monkey-patches the `jira` SDK so that
no HTTP requests are made.
"""

import json
import sys
import types

import llm

# ---------------------------------------------------------------------------
# 1.  Monkey-patch the `jira` module *before* importing the plugin
# ---------------------------------------------------------------------------

# Create a dummy `jira` package with the minimal surface we need
jira_stub = types.ModuleType("jira")


class _FakeIssue:
    def __init__(self, key="ENG-123"):
        self.key = key


class _FakeJIRA:
    def __init__(self, *args, **kwargs):
        # Nothing to do – we’re a stub
        pass

    def create_issue(self, *, fields):
        # Return a predictable key so the assertion is easy
        return _FakeIssue()


jira_stub.JIRA = _FakeJIRA
sys.modules["jira"] = jira_stub  # Must happen before importing the toolbox

# ---------------------------------------------------------------------------
# 2.  Now we can safely import the toolbox
# ---------------------------------------------------------------------------

from llm_tools_jira import Jira  # noqa: E402 – needs the monkey-patch above


def _toolbox():
    """
    Return a Jira toolbox instance whose API client is the stub defined
    above.  We pass dummy credentials so __init__ doesn’t look at
    `llm.get_key()`.
    """
    tb = Jira(
        server="https://example.atlassian.net",
        email="me@example.com",
        api_token="dummy",
    )
    # Make doubly sure the stub client is used
    tb._jira = _FakeJIRA()
    return tb


# ---------------------------------------------------------------------------
# 3.  The actual test
# ---------------------------------------------------------------------------


def test_jira_create_issue_tool():
    model = llm.get_model("echo")
    toolbox = _toolbox()

    chain_response = model.chain(
        json.dumps(
            {
                "prompt": "Create a Jira ticket",
                "tool_calls": [
                    {
                        # Tool names for toolboxes are ClassName_methodName
                        # – here that’s Jira_create_issue
                        "name": "Jira_create_issue",
                        "arguments": {
                            "project_key": "ENG",
                            "summary": "Example summary",
                            "description": "Example description",
                        },
                    }
                ],
            }
        ),
        tools=[toolbox],
    )

    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]

    assert tool_results == [
        {
            "name": "Jira_create_issue",
            "output": "ENG-123",
            "tool_call_id": None,
        }
    ]
