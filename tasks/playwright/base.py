"""
A part of the task implementation is borrowed from LangChain: 
https://github.com/langchain-ai/langchain
"""
from __future__ import annotations
from tasks.task import BaseTask
from typing import TYPE_CHECKING, Optional, Dict, Any
from pydantic import model_validator
from tasks.playwright.utils import create_sync_playwright_browser
import asyncio

if TYPE_CHECKING:
    from playwright.sync_api import Browser as SyncBrowser
else:
    try:
        # We do this so pydantic can resolve the types when instantiating
        from playwright.sync_api import Browser as SyncBrowser
    except ImportError:
        pass

class BaseBrowser(BaseTask):
	sync_browser: Optional[Any] = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		if "sync_browser" in kwargs:
			self.sync_browser = kwargs["sync_browser"]
		if self.sync_browser is None:
			raise ValueError("Either async_browser or sync_browser must be specified.")


	@model_validator(mode='before')
	def validate_environment(cls, values: Dict) -> Dict:
		"""Validate that api key and python package exists in environment."""
		try:
			from playwright.sync_api import Browser as SyncBrowser  # noqa: F401        
		except ImportError:
			raise ImportError(
					"The 'playwright' package is required to use the playwright tools."
					" Please install it with 'pip install playwright'."
			)
		return values