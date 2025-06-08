import llm
import json
from llm_tools_jira import create_issue


def test_tool():
    model = llm.get_model("echo")
    chain_response = model.chain(
        json.dumps(
            {
                "tool_calls": [
                    {"name": "create_issue", "arguments": {"input": "pelican"}}
                ]
            }
        ),
        tools=[create_issue],
    )
    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]
    assert tool_results == [
        {"name": "create_issue", "output": "hello pelican", "tool_call_id": None}
    ]
