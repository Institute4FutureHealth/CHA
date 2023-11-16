from tasks.playwright.base import BaseBrowser
from typing import List, Any
from tasks.playwright.utils import (
    get_current_page,
)
from urllib.parse import urlparse


class NavigateBack(BaseBrowser):
  name: str = "navigate_back"
  chat_name: str = "NavigateBack"
  description: str = (
    "Navigate back to the previous page in the browser history"     
  )
  dependencies: List[str] = []
  inputs: List[str] = ["url to navigate to"]
  outputs: List[str] = []
  output_type: bool = False

  def validate_url(self, url):
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be 'http' or 'https'")
    return url

  def _execute(
    self,
    inputs: List[Any],
  ) -> str:
    if self.sync_browser is None:
      raise ValueError(f"Synchronous browser not provided to {self.name}")
    page = get_current_page(self.sync_browser)
    response = page.go_back()

    if response:
      return (
        f"Navigated back to the previous page with URL '{response.url}'."
        f" Status code {response.status}"
      )
    else:
      return "Unable to navigate back; no previous page in the history"

  def explain(
        self,
      ) -> str:
    return (
      "This task extracts all of the hyperlinks."
    )