from typing import Any
from typing import List

from pydantic import Extra
from pydantic import Field
from pydantic import model_validator

from tasks.playwright.base import BaseBrowser
from tasks.playwright.utils import (
    get_current_page,
)
from utils import get_from_dict_or_env


class Click(BaseBrowser):
    """
    **Description:**

        This code defines a class named Click that inherits from the BaseBrowser class.
        The Click class represents a task related to browser interactions, specifically clicking on an element
        identified by a CSS selector using the Playwright library.

    """

    name: str = "click"
    chat_name: str = "Clicker"
    description: str = (
        "Click on an element with the given CSS selector"
    )
    dependencies: List[str] = []
    inputs: List[str] = ["CSS selector for the element to click"]
    outputs: List[str] = []
    output_type: bool = False

    def _selector_effective(self, selector: str) -> str:
        """
            Get the effective CSS selector considering visibility.

        Args:
            selector (str): The original CSS selector.
        Return:
            str: The effective CSS selector.

        """

        if not self.visible_only:
            return selector
        return f"{selector} >> visible=1"

    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        """
            Execute the click task by clicking on an element with the provided CSS selector.

        Aegs:
            input (str): The input string containing the CSS selector.
        Return:
            str: A message indicating the success or failure of the click operation.

        """
        selector = inputs[0]
        if self.sync_browser is None:
            raise ValueError(
                f"Synchronous browser not provided to {self.name}"
            )
        page = get_current_page(self.sync_browser)
        # Navigate to the desired webpage before using this tool
        selector_effective = self._selector_effective(
            selector=selector
        )
        from playwright.sync_api import (
            TimeoutError as PlaywrightTimeoutError,
        )

        try:
            page.click(
                selector_effective,
                strict=self.playwright_strict,
                timeout=self.playwright_timeout,
            )
        except PlaywrightTimeoutError:
            return f"Unable to click on element '{selector}'"
        return f"Clicked element '{selector}'"

    def explain(
        self,
    ) -> str:
        """
            Explain the purpose of the click task.

        Return:
            str: A brief explanation of the task.

        """

        return "This task clicks on an element in an specific url"
