from typing import Any
from typing import List
from urllib.parse import urlparse

from tasks.playwright.base import BaseBrowser
from tasks.playwright.utils import (
    get_current_page,
)


class NavigateBack(BaseBrowser):
    """
    **Description:**

        This class represents a browser navigation task using Playwright.
    """

    name: str = "navigate_back"
    chat_name: str = "NavigateBack"
    description: str = (
        "Navigate back to the previous page in the browser history"
    )
    dependencies: List[str] = []
    inputs: List[str] = ["url to navigate to"]
    outputs: List[str] = []
    output_type: bool = False

    def validate_url(self, url):
        """
            This method validates a given URL by checking if its scheme is either 'http' or 'https'.

        Args:
            url (str): The URL to be validated.
        Return:
            str: The validated URL.
        Raise:
            ValueError: If the URL scheme is not 'http' or 'https'.

        """

        parsed_url = urlparse(url)
        if parsed_url.scheme not in ("http", "https"):
            raise ValueError("URL scheme must be 'http' or 'https'")
        return url

    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        """
            This method executes the navigation back action in the browser using Playwright.

        Args:
            input (str): The input string containing the URL to navigate to.
        Return:
            str:    A message indicating whether the navigation was successful, including the URL and status code if successful,
                    or an error message if unsuccessful.

        """
        if self.sync_browser is None:
            raise ValueError(
                f"Synchronous browser not provided to {self.name}"
            )
        page = get_current_page(self.sync_browser)
        response = page.go_back()

        if response:
            return (
                f"Navigated back to the previous page with URL '{response.url}'."
                f" Status code {response.status}"
            )
        else:
            return "Unable to navigate back; no previous page in the history"

    def explain(
        self,
    ) -> str:
        """
            This method provides an explanation of the task.

        Return:
            str: A brief explanation of the task, in this case, "This task extracts all of the hyperlinks."


        """

        return "This task extracts all of the hyperlinks."
