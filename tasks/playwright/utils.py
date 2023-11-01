from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Browser as SyncBrowser
    from playwright.sync_api import Page as SyncPage

def get_current_page(browser: SyncBrowser) -> SyncPage:
    if not browser.contexts:
        context = browser.new_context()
        return context.new_page()
    context = browser.contexts[0]  # Assuming you're using the default browser context
    if not context.pages:
        return context.new_page()
    # Assuming the last page in the list is the active one
    return context.pages[-1]

def create_sync_playwright_browser(headless: bool = True) -> SyncBrowser:
    from playwright.sync_api import sync_playwright

    browser = sync_playwright().start()
    return browser.chromium.launch(headless=headless)