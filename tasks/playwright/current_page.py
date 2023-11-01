from tasks.playwright.base import BaseBrowser
from typing import List
from tasks.playwright.utils import (
    get_current_page,
)

class CurrentWebPage(BaseBrowser):
  name: str = "current_webpage"
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
    inputs = self.parse_input(input)
    if self.sync_browser is None:
      raise ValueError(f"Synchronous browser not provided to {self.name}")
    page = get_current_page(self.sync_browser)
    return str(page.url)

  def explain(
        self,
      ) -> str:
    return (
      "This task returns the ulr of the current page."
    )