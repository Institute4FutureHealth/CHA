from tasks.playwright.base import BaseBrowser
from typing import List
from tasks.playwright.utils import (
    get_current_page,
)


class CurrentWebPage(BaseBrowser):
    name: str = "current_page"
    chat_name: str = "CurrentPage"
    description: str = (
        "Returns the URL of the current page"
    )
    dependencies: List[str] = []
    inputs: List[str] = []
    outputs: List[str] = []
    output_type: bool = False

    def execute(
            self,
            input: str,
    ) -> str:
        """
        Execute the current_page task by retrieving the URL of the current web page.

        Args:
            input (str): The input string (not used in this task).
        Return:
            str: The URL of the current web page.
        Raise:
            ValueError: If the synchronous browser is not provided.

        """

        inputs = self.parse_input(input)
        if self.sync_browser is None:
            raise ValueError(f"Synchronous browser not provided to {self.name}")
        page = get_current_page(self.sync_browser)
        return str(page.url)

    def explain(
            self,
    ) -> str:
        """
        Provide a brief explanation of the current_page task.

        Return:
            str: An explanation of the task.

        """

        return (
            "This task returns the ulr of the current page."
        )
