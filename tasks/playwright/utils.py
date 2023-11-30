from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Browser as SyncBrowser
    from playwright.sync_api import Page as SyncPage


def get_current_page(browser: SyncBrowser) -> SyncPage:
    """
    This function retrieves the current page from a given Playwright synchronous browser instance.

    Args:
        browser (SyncBrowser): An instance of the Playwright synchronous browser.
    Return:
        SyncPage: The current page from the provided browser.

    """

    if not browser.contexts:
        context = browser.new_context()
        return context.new_page()
    context = browser.contexts[
        0
    ]  # Assuming you're using the default browser context
    if not context.pages:
        return context.new_page()
    # Assuming the last page in the list is the active one
    return context.pages[-1]


def create_sync_playwright_browser(
    headless: bool = True,
) -> SyncBrowser:
    """
    This function creates and launches a Playwright synchronous browser.

    Args:
        headless (bool, optional): Whether to launch the browser in headless mode. Default is True.
    Return:
        SyncBrowser: The created Playwright synchronous browser instance.

    """

    from playwright.sync_api import sync_playwright

    browser = sync_playwright().start()
    return browser.chromium.launch(headless=headless)
