import json
from typing import Any
from typing import List

from pydantic import model_validator

from tasks.playwright.base import BaseBrowser
from tasks.playwright.utils import (
    get_current_page,
)


class ExtractHyperlinks(BaseBrowser):
    """
    **Description:**

        This task extracts all hyperlinks from the current webpage.
    """

    name: str = "extract_hyperlinks"
    chat_name: str = "ExtractHyperLinks"
    description: str = "Extract all hyperlinks on the current webpage"
    dependencies: List[str] = []
    inputs: List[str] = [
        "Boolean: True/False. Return absolute URLs instead of relative URLs."
    ]
    outputs: List[str] = []
    output_type: bool = False

    @model_validator(mode="before")
    def check_bs_import(cls, values: dict) -> dict:
        """
            Check that the arguments are valid.

        Args:
            values (Dict): The current attribute values.
        Return:
            Dict: The updated attribute values.
        Raise:
            ImportError: If 'beautifulsoup4' package is not installed.

        """

        try:
            from bs4 import BeautifulSoup  # noqa: F401
        except ImportError:
            raise ImportError(
                "The 'beautifulsoup4' package is required to use this tool."
                " Please install it with 'pip install beautifulsoup4'."
            )
        return values

    @staticmethod
    def scrape_page(
        page: Any, html_content: str, absolute_urls: bool
    ) -> str:
        """
            Scrape hyperlinks from the current webpage.

        Args:
            page (Any): The current webpage.
            html_content (str): The HTML content of the webpage.
            absolute_urls (bool): True if absolute URLs should be returned, False otherwise.
        Return:
            str: JSON string containing the extracted hyperlinks.


        """

        from urllib.parse import urljoin
        from bs4 import BeautifulSoup

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, "lxml")

        # Find all the anchor elements and extract their href attributes
        anchors = soup.find_all("a")
        if absolute_urls:
            base_url = page.url
            links = [
                urljoin(base_url, anchor.get("href", ""))
                for anchor in anchors
            ]
        else:
            links = [anchor.get("href", "") for anchor in anchors]
        # Return the list of links as a JSON string
        return json.dumps(links)

    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        """
            Execute the ExtractHyperlinks task.

        Args:
            input (str): The input parameter for the task.
        Return:
            str: JSON string containing the extracted hyperlinks.
        Raise:
            ValueError: If the synchronous browser is not provided.

        """
        if self.sync_browser is None:
            raise ValueError(
                f"Synchronous browser not provided to {self.name}"
            )
        page = get_current_page(self.sync_browser)
        html_content = page.content()
        return self.scrape_page(page, html_content, inputs[0])

    def explain(
        self,
    ) -> str:
        """
            Provide a brief explanation of the ExtractHyperlinks task.

        Return:
            str: An explanation of the task.


        """

        return "This task extracts all of the hyperlinks."
