from __future__ import annotations

import json
from typing import Any
from typing import List
from typing import Optional
from typing import Sequence
from typing import TYPE_CHECKING

from pydantic import model_validator

from tasks.playwright.base import BaseBrowser
from tasks.playwright.utils import (
    get_current_page,
)

if TYPE_CHECKING:
    from playwright.sync_api import Page as SyncPage


class GetElements(BaseBrowser):
    """
    **Description:**

        The GetElements class is a subclass of BaseBrowser responsible for retrieving elements
        on the current web page that match a given CSS selector.
    """

    name: str = "get_elements"
    chat_name: str = "GetElements"
    description: str = "Retrieve elements in the current web page matching the given CSS selector"
    dependencies: List[str] = []
    inputs: List[str] = [
        "CSS selector, such as '*', 'div', 'p', 'a', #id, .classname",
        "Set of attributes to retrieve for each element",
    ]
    outputs: List[str] = []
    output_type: bool = False

    def _get_elements(
        page: SyncPage, selector: str, attributes: Sequence[str]
    ) -> List[dict]:
        """
            Get elements matching the given CSS selector.

        Args:
            page (SyncPage): The current page.
            selector (str): CSS selector to match elements.
            attributes (Sequence[str]): Set of attributes to retrieve for each element.
        Return:
            List[dict]: A list of dictionaries containing the retrieved elements and their attributes.


        """

        elements = page.query_selector_all(selector)
        results = []
        for element in elements:
            result = {}
            for attribute in attributes:
                if attribute == "innerText":
                    val: Optional[str] = element.inner_text()
                else:
                    val = element.get_attribute(attribute)
                if val is not None and val.strip() != "":
                    result[attribute] = val
            if result:
                results.append(result)
        return results

    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        """
            Execute the GetElements task.

        Args:
            input (str): Input string containing CSS selector and attributes.
        Return:
            str: The JSON-formatted string containing the retrieved elements and their attributes.
        Raise:
            ValueError: If the synchronous browser is not provided.


        """
        if self.sync_browser is None:
            raise ValueError(
                f"Synchronous browser not provided to {self.name}"
            )
        page = get_current_page(self.sync_browser)
        # Navigate to the desired webpage before using this tool
        results = self._get_elements(page, inputs[0], inputs[1])
        return json.dumps(results, ensure_ascii=False)

    def explain(
        self,
    ) -> str:
        """
            Explain the GetElements task.

        Return:
            str: A brief explanation of the GetElements task.

        """

        return "This task gets the elements."
