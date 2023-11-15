from tasks.playwright.base import BaseBrowser
from typing import List
from tasks.playwright.utils import (
    get_current_page,
)
from pydantic import model_validator


class ExtractText(BaseBrowser):
    name: str = "extract_text"
    chat_name: str = "ExtractText"
    description: str = (
        "Extract all the text on the current webpage"
    )
    dependencies: List[str] = ["navigate"]
    inputs: List[str] = ["no input"]
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



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

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



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        from bs4 import BeautifulSoup

        if self.sync_browser is None:
            raise ValueError(f"Synchronous browser not provided to {self.name}")
        print("sync browser", self.sync_browser)
        page = get_current_page(self.sync_browser)
        if page.url == "about:blank":
            return f"call {self.dependencies} first."
        html_content = page.content()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, "lxml")

        return " ".join(text for text in soup.stripped_strings)

    def explain(
            self,
    ) -> str:
        """
        Explain the ExtractText task.

        Return:
            str: A brief explanation of the ExtractText task.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        return (
            "This task returns the ulr of the current page."
        )
