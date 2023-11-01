"""
A part of the task implementation is borrowed from LangChain: 
https://github.com/langchain-ai/langchain
"""
from __future__ import annotations
from tasks.task import BaseTask
from typing import TYPE_CHECKING, Optional, Dict
from pydantic import model_validator
from tasks.playwright.utils import create_sync_playwright_browser

if TYPE_CHECKING:
    from playwright.sync_api import Browser as SyncBrowser
else:
    try:
        # We do this so pydantic can resolve the types when instantiating
        from playwright.sync_api import Browser as SyncBrowser
    except ImportError:
        pass

class BaseBrowser(BaseTask):
  sync_browser: Optional["SyncBrowser"] = None

  @model_validator(mode='before')
  def validate_environment(cls, values: Dict) -> Dict:
    """Validate that api key and python package exists in environment."""
    try:
        from playwright.sync_api import Browser as SyncBrowser  # noqa: F401
        values["sync_browser"] = create_sync_playwright_browser()
    except ImportError:
        raise ImportError(
            "The 'playwright' package is required to use the playwright tools."
            " Please install it with 'pip install playwright'."
        )
    if values.get("sync_browser") is None:
        raise ValueError("Either async_browser or sync_browser must be specified.")
    return values