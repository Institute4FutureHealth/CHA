from tasks.playwright.base import BaseBrowser
from typing import List
from tasks.playwright.utils import (
    get_current_page,
)
from pydantic import model_validator

class ExtractText(BaseBrowser):
  name: str = "extract_text"
  chat_name: str = "ExtractText"
  description: str = (
    "Extract all the text on the current webpage"     
  )
  dependencies: List[str] = []
  inputs: List[str] = []
  outputs: List[str] = []
  output_type: bool = False

  @model_validator(mode="before")
  def check_acheck_bs_importrgs(cls, values: dict) -> dict:
    """Check that the arguments are valid."""
    try:
      from bs4 import BeautifulSoup  # noqa: F401
    except ImportError:
      raise ImportError(
        "The 'beautifulsoup4' package is required to use this tool."
        " Please install it with 'pip install beautifulsoup4'."
      )
    return values

  def execute(
    self,
    input: str,
  ) -> str:
    inputs = self.parse_input(input)
    from bs4 import BeautifulSoup

    if self.sync_browser is None:
      raise ValueError(f"Synchronous browser not provided to {self.name}")

    page = get_current_page(self.sync_browser)
    html_content = page.content()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, "lxml")

    return " ".join(text for text in soup.stripped_strings)

  def explain(
        self,
      ) -> str:
    return (
      "This task returns the ulr of the current page."
    )