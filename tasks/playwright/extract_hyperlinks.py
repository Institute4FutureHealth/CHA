from tasks.playwright.base import BaseBrowser
from typing import List, Any
from tasks.playwright.utils import (
    get_current_page,
)
from pydantic import model_validator
import json

class ExtractHyperlinks(BaseBrowser):
  name: str = "extract_hyperlinks"
  chat_name: str = "ExtractHyperLinks"
  description: str = (
    "Extract all hyperlinks on the current webpage"     
  )
  dependencies: List[str] = []
  inputs: List[str] = ["Boolean: True/False. Return absolute URLs instead of relative URLs."]
  outputs: List[str] = []
  output_type: bool = False

  @model_validator(mode='before')
  def check_bs_import(cls, values: dict) -> dict:
    """Check that the arguments are valid."""
    try:
        from bs4 import BeautifulSoup  # noqa: F401
    except ImportError:
        raise ImportError(
            "The 'beautifulsoup4' package is required to use this tool."
            " Please install it with 'pip install beautifulsoup4'."
        )
    return values

  @staticmethod
  def scrape_page(page: Any, html_content: str, absolute_urls: bool) -> str:
    from urllib.parse import urljoin
    from bs4 import BeautifulSoup

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, "lxml")

    # Find all the anchor elements and extract their href attributes
    anchors = soup.find_all("a")
    if absolute_urls:
        base_url = page.url
        links = [urljoin(base_url, anchor.get("href", "")) for anchor in anchors]
    else:
        links = [anchor.get("href", "") for anchor in anchors]
    # Return the list of links as a JSON string
    return json.dumps(links)

  def execute(
    self,
    input: str,
  ) -> str:
    inputs = self.parse_input(input)
    if self.sync_browser is None:
      raise ValueError(f"Synchronous browser not provided to {self.name}")
    page = get_current_page(self.sync_browser)
    html_content = page.content()
    return self.scrape_page(page, html_content, inputs[0])

  def explain(
        self,
      ) -> str:
    return (
      "This task extracts all of the hyperlinks."
    )