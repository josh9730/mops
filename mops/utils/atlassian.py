import keyring
from atlassian import Jira, Confluence


class Atlassian:
    """Base class for Jira & Confluence methods."""

    def __init__(self):
        jira_url = keyring.get_password("jira", "url")
        confluence_url = keyring.get_password("confl", "url")
        username = keyring.get_password("cas", "user")
        password = keyring.get_password("cas", username)

        self.jira = Jira(
            url=jira_url,
            username=username,
            password=password,
        )
        self.confluence = Confluence(
            url=confluence_url,
            username=username,
            password=password,
        )

    def jira_projects_list(self) -> list:
        """Return list of Jira Projects."""
        projects = self.jira.projects(included_archived=None)
        return [project["key"] for project in projects]

    def jira_create_link(self, link_data: list) -> None:
        """Link Jira ticket to Confluence page.

        The Jira macro supplied in the Confluence template only creates a
        unidirectional link Confluence -> Jira. This method creates a link
        Jira -> Confluence.

        link_data:
          ticket: str
          link_title: url
          page_title: str
        """
        self.jira.create_or_update_issue_remote_links(
            *link_data, relationship="mentioned in"
        )

    def confluence_create_or_update(self, page_data: tuple) -> None:
        """Create or Update Confluence page.

        page_data: list in the form of:
          parent_page_id: int
          page_title: str
          rendered_mop: str, in Confluence Wiki format
        """
        self.confluence.update_or_create(*page_data, representation="wiki")
