"""
A part of the task implementation is borrowed from LangChain:
https://github.com/langchain-ai/langchain
"""
from __future__ import annotations

from typing import Any
from typing import Dict
from typing import Optional
from typing import TYPE_CHECKING

from pydantic import model_validator

from tasks.playwright.utils import create_sync_playwright_browser
from tasks.task import BaseTask

if TYPE_CHECKING:
    from playwright.sync_api import Browser as SyncBrowser
else:
    try:
        # We do this so pydantic can resolve the types when instantiating
        from playwright.sync_api import Browser as SyncBrowser
    except ImportError:
        pass


class BaseBrowser(BaseTask):
    """
    **Description:**

        This code defines a base class named BaseBrowser that inherits from BaseTask.
        This class is intended for tasks related to browser interactions using the Playwright library.
        The code uses conditional imports to handle situations where the Playwright library is not available.
    """

    sync_browser: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "sync_browser" in kwargs:
            self.sync_browser = kwargs["sync_browser"]
        if self.sync_browser is None:
            raise ValueError(
                "Either async_browser or sync_browser must be specified."
            )

    @model_validator(mode="before")
    def validate_environment(cls, values: Dict) -> Dict:
        """
            Validate that api key and python package exists in environment.

        Args:
            cls (object): The class itself.
            values (Dict): The dictionary containing the values for validation.
        Return:
            Dict:The original values.
        Raise:
            ImportError: If the 'playwright' package is not installed.

        """

        try:
            from playwright.sync_api import (
                Browser as SyncBrowser,
            )  # noqa: F401
        except ImportError:
            raise ImportError(
                "The 'playwright' package is required to use the playwright tools."
                " Please install it with 'pip install playwright'."
            )
        return values
