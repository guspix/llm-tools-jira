import llm


def create_issue(input: str) -> str:
    """
    Description of tool goes here.
    """
    return f"hello {input}"


@llm.hookimpl
def register_tools(register):
    register(create_issue)
