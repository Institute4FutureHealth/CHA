from __future__ import annotations
from tasks.playwright.base import BaseBrowser
from typing import TYPE_CHECKING, List, Sequence, Optional, Any
from tasks.playwright.utils import (
    get_current_page,
)
from pydantic import model_validator
import json
if TYPE_CHECKING:
    from playwright.sync_api import Page as SyncPage

class GetElements(BaseBrowser):
  name: str = "get_elements"
  chat_name: str = "GetElements"
  description: str = (
    "Retrieve elements in the current web page matching the given CSS selector"     
  )
  dependencies: List[str] = []
  inputs: List[str] = [
    "CSS selector, such as '*', 'div', 'p', 'a', #id, .classname",
    "Set of attributes to retrieve for each element"
  ]
  outputs: List[str] = []
  output_type: bool = False

  def _get_elements(
    page: SyncPage, selector: str, attributes: Sequence[str]
  ) -> List[dict]:
    """Get elements matching the given CSS selector."""
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
    if self.sync_browser is None:
      raise ValueError(f"Synchronous browser not provided to {self.name}")
    page = get_current_page(self.sync_browser)
    # Navigate to the desired webpage before using this tool
    results = self._get_elements(page, inputs[0], inputs[1])
    return json.dumps(results, ensure_ascii=False)

  def explain(
        self,
      ) -> str:
    return (
      "This task gets the elements."
    )