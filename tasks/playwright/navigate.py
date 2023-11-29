from typing import Any
from typing import List
from urllib.parse import urlparse

from tasks.playwright.base import BaseBrowser
from tasks.playwright.utils import (
    get_current_page,
)


class Navigate(BaseBrowser):
    """
    **Description:**

        This class represents a browser navigation task to a specified URL using Playwright.
    """

    name: str = "navigate"
    chat_name: str = "Navigate"
    description: str = "Navigate a browser to the specified URL"
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
            This method executes the navigation action in the browser using Playwright.

        Args:
            input (str): The input string containing the URL to navigate to.
        Return:
            str:    A message indicating whether the navigation was successful, including the URL and status code if successful,
                    or an error message if unsuccessful.

        """
        self.validate_url(inputs[0].strip())
        if self.sync_browser is None:
            raise ValueError(
                f"Synchronous browser not provided to {self.name}"
            )
        page = get_current_page(self.sync_browser)
        response = page.goto(inputs[0])
        status = response.status if response else "unknown"
        return (
            f"Navigating to {inputs[0]} returned status code {status}"
        )

    def explain(
        self,
    ) -> str:
        """
            This method provides an explanation of the task.

        Return:
            str: A brief explanation of the task, in this case, "This task extracts all of the hyperlinks."

        """

        return "This task extracts all of the hyperlinks."
