"""
LLM Toolbox for working with Jira
---------------------------------

Provides a single tool for now – ``Jira_create_issue`` – exposed from the
:class:`Jira` toolbox below.  Additional methods you add (e.g. ``comment``,
``transition``) will automatically become new tools so long as their names
*don’t* start with an underscore.

Save Jira credentials with::

    llm keys set jira-server https://example.atlassian.net
    llm keys set jira-email  me@example.com
    llm keys set jira-api-token  ******

Usage from the CLI while you iterate::

    llm -T Jira_create_issue "Open a new ENG Task" --td \
        --json '{"project_key": "ENG",
                 "summary": "Fix login bug",
                 "description": "Users cannot …"}'
"""

from __future__ import annotations

from typing import Any, Dict

import llm
from jira import JIRA

__all__ = ["Jira"]


class Jira(llm.Toolbox):
    """
    A toolbox that exposes Jira-related tools.

    Parameters
    ----------
    server, email, api_token
        Optional explicit credentials; if omitted we fall back to
        values stored with :command:`llm keys set`.
    """

    def __init__(
        self,
        *,
        server: str | None = None,
        email: str | None = None,
        api_token: str | None = None,
    ):
        # Pull from llm keys unless the caller supplied overrides
        self.server = server or llm.get_key("jira-server")
        self.email = email or llm.get_key("jira-email")
        self.api_token = api_token or llm.get_key("jira-api-token")

        if not all((self.server, self.email, self.api_token)):
            raise RuntimeError(
                "Missing Jira credentials – run `llm keys set jira-server`, "
                "`jira-email`, and `jira-api-token` first."
            )

        # One authenticated client, re-used for every tool invocation
        self._jira = JIRA(server=self.server, basic_auth=(self.email, self.api_token))

    # ------------------------------- TOOLS -------------------------------- #

    def create_issue(
        self,
        project_key: str,
        summary: str,
        description: str,
        issue_type: str = "Task",
    ) -> str:
        """
        Create an issue in Jira and return its key.

        Parameters
        ----------
        project_key
            The target project (e.g. ``"ENG"``).
        summary
            One-line summary/subject.
        description
            Full markdown-friendly description body.
        issue_type
            Jira issue type – defaults to ``"Task"``; common alternatives
            are ``"Bug"``, ``"Story"``, or any custom type your instance
            defines.

        Returns
        -------
        str
            The new issue key, e.g. ``"ENG-1234"``.
        """
        fields: Dict[str, Any] = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
        }
        issue = self._jira.create_issue(fields=fields)
        return issue.key


# --------------------------- Plugin registration --------------------------- #


@llm.hookimpl
def register_tools(register):  # type: ignore[override]
    """
    Register the :class:`Jira` toolbox with LLM.
    """
    register(Jira)
