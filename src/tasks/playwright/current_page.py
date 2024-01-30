from typing import Any
from typing import List

from tasks.playwright.base import BaseBrowser
from tasks.playwright.utils import (
    get_current_page,
)


class CurrentWebPage(BaseBrowser):
    """
    **Description:**

        This code defines a class named CurrentWebPage that inherits from the BaseBrowser class.
        The CurrentWebPage class represents a task related to browser interactions, specifically retrieving the URL of the current web page.

    """

    name: str = "current_page"
    chat_name: str = "CurrentPage"
    description: str = "Returns the URL of the current page"
    dependencies: List[str] = []
    inputs: List[str] = []
    outputs: List[str] = []
    output_type: bool = False

    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        """
            This method executes the task by retrieving the current page from the synchronous browser using
            the get_current_page function and returning its URL.

        Args:
            input (str): The input string (not used in this task).
        Return:
            str: The URL of the current web page.
        Raise:
            ValueError: If the synchronous browser is not provided.

        """
        if self.sync_browser is None:
            raise ValueError(
                f"Synchronous browser not provided to {self.name}"
            )
        page = get_current_page(self.sync_browser)
        return str(page.url)

    def explain(
        self,
    ) -> str:
        """
            Provides a brief explanation of the current_page task.

        Return:
            str: An explanation of the task.

        """

        return "This task returns the ulr of the current page."
