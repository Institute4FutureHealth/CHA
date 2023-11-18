from tasks.playwright.base import BaseBrowser
from typing import List
from tasks.playwright.utils import (
    get_current_page,
)
from pydantic import model_validator
from urllib.parse import urlparse


class ExtractText(BaseBrowser):
    """
    **Description:** 

        This task extracts all the text from the current webpage.
    """
    name: str = "extract_text"
    chat_name: str = "ExtractText"
    description: str = (
        "Extract all the text on the current webpage"
    )
    dependencies: List[str] = ["navigate"]
    inputs: List[str] = ["url to navigate to"]
    outputs: List[str] = []
    output_type: bool = False

    @model_validator(mode="before")
    def check_acheck_bs_importrgs(cls, values: dict) -> dict:
        """
            Check that the arguments are valid.

        Args:
            values (Dict): The current attribute values.
        Return:
            Dict: The updated attribute values.
        Raise:
            ImportError: If 'beautifulsoup4' or 'lxml' packages are not installed.

        """

        try:
            from bs4 import BeautifulSoup  # noqa: F401
        except ImportError:
            raise ImportError(
                "The 'beautifulsoup4' package is required to use this tool."
                " Please install it with 'pip install beautifulsoup4'."
            )

        try:
            import lxml  # noqa: F401
        except ImportError:
            raise ImportError(
                "The 'lxml' package is required to use this tool."
                " Please install it with 'pip install lxml'."
            )
        return values

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

    def execute(
            self,
            input: str,
    ) -> str:
        """
            Execute the ExtractText task.

        Args:
            input (str): The input parameter for the task.
        Return:
            str: The extracted text from the current webpage.
        Raise:
            ValueError: If the synchronous browser is not provided.

        """

        from bs4 import BeautifulSoup

        inputs = self.parse_input(input)
        self.validate_url(inputs[0].strip())

        if self.sync_browser is None:
            raise ValueError(f"Synchronous browser not provided to {self.name}")

        page = get_current_page(self.sync_browser)
        response = page.goto(inputs[0])
        status = response.status if response else "unknown"

        if status == 200:
            html_content = page.content()
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, "lxml")

            return " ".join(text for text in soup.stripped_strings)
        else:
            return "Error extracting text. The url is wrong. Try again."

    def explain(
            self,
    ) -> str:
        """
            Explain the ExtractText task.

        Return:
            str: A brief explanation of the ExtractText task.


        """

        return (
            "This task returns the ulr of the current page."
        )
