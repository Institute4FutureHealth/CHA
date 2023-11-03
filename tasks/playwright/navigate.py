from tasks.playwright.base import BaseBrowser
from typing import List
from tasks.playwright.utils import (
    get_current_page,
)
from urllib.parse import urlparse


class Navigate(BaseBrowser):
  name: str = "navigate"
  chat_name: str = "Navigate"
  description: str = (
    "Navigate a browser to the specified URL"     
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

  def execute(
    self,
    input: str,
  ) -> str:
    inputs = self.parse_input(input)
    self.validate_url(inputs[0])
    if self.sync_browser is None:
      raise ValueError(f"Synchronous browser not provided to {self.name}")
    page = get_current_page(self.sync_browser)
    response = page.goto(inputs[0])
    status = response.status if response else "unknown"
    return f"Navigating to {inputs[0]} returned status code {status}"

  def explain(
        self,
      ) -> str:
    return (
      "This task extracts all of the hyperlinks."
    )