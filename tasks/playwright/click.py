from tasks.playwright.base import BaseBrowser
from typing import Any, Optional, List, Dict
from utils import get_from_dict_or_env
from pydantic import Field, model_validator, Extra
from tasks.playwright.utils import (
    get_current_page,
)

class Click(BaseBrowser):
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
    if not self.visible_only:
      return selector
    return f"{selector} >> visible=1"

  def _execute(
    self,
    inputs: List[Any],
  ) -> str:
    selector = inputs[0]
    if self.sync_browser is None:
        raise ValueError(f"Synchronous browser not provided to {self.name}")
    page = get_current_page(self.sync_browser)
    # Navigate to the desired webpage before using this tool
    selector_effective = self._selector_effective(selector=selector)
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

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
    return (
      "This task clicks on an element in an specific url"
    )