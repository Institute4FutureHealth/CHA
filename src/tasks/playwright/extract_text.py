import io
from typing import Any
from typing import List
from urllib.parse import urlparse

import requests
from pydantic import model_validator

from tasks.playwright.base import BaseBrowser
from tasks.playwright.utils import (
    get_current_page,
)


class ExtractText(BaseBrowser):
    """
    **Description:**

        This task extracts all the text from the current webpage.
    """

    name: str = "extract_text"
    chat_name: str = "ExtractText"
    description: str = "Extract all the text on the current webpage"
    dependencies: List[str] = []
    inputs: List[str] = [
        "url to extract the text from. It requires links which is gathered from other tools. Never provide urls on your own."
    ]
    outputs: List[str] = [
        "An string containing the text of the scraped webpage."
    ]
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
            ImportError: If 'beautifulsoup4', 'lxml', or 'pdfminer' packages are not installed.

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

        try:
            from pdfminer import high_level  # noqa: F401
        except ImportError:
            raise ImportError(
                "The 'pdfminer' package is required to use this tool."
                " Please install it with 'pip install pdfminer.six'."
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

    def _execute(
        self,
        inputs: List[Any],
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
        from pdfminer import high_level

        self.validate_url(inputs[0].strip())

        if self.sync_browser is None:
            raise ValueError(
                f"Synchronous browser not provided to {self.name}"
            )

        if inputs[0].lower().endswith(".pdf"):
            # Request the PDF content from the URL
            response = requests.get(inputs[0])
            if response.status_code == 200:
                # Use BytesIO to create an in-memory stream
                pdf_stream = io.BytesIO(response.content)
                # Extract text from the PDF stream
                text = high_level.extract_text(pdf_stream)
                # Wrap text in basic HTML tags
                html_content = (
                    f"<html><body><p>{text}</p></body></html>"
                )
                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(html_content, "lxml")
                return " ".join(
                    text for text in soup.stripped_strings
                )
            else:
                return "Error extracting text. The url is wrong. Try again."
        else:
            page = get_current_page(self.sync_browser)
            response = page.goto(inputs[0])
            status = response.status if response else "unknown"

            if status == 200:
                html_content = page.content()
                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(html_content, "lxml")
                page.close()
                return " ".join(
                    text for text in soup.stripped_strings
                )
            else:
                page.close()
                return "Error extracting text. The url is wrong. Try again."

    def explain(
        self,
    ) -> str:
        """
            Explain the ExtractText task.

        Return:
            str: A brief explanation of the ExtractText task.


        """

        return "This task returns the ulr of the current page."
