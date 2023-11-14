Utils
=====






The provided code includes utility functions related to Playwright for synchronous browser automation.


- ``get_current_page`` : This function retrieves the current page from a given Playwright synchronous browser instance.

    .. py:function:: get_current_page(browser: SyncBrowser)

        This function retrieves the current page from a given Playwright synchronous browser instance.

        :param browser: An instance of the Playwright synchronous browser.
        :type browser: SyncBrowser
        :return: The current page from the provided browser.
        :rtype: SyncPage


|


- ``create_sync_playwright_browser`` : This function creates and launches a Playwright synchronous browser.

    .. py:function:: create_sync_playwright_browser(headless: bool = True)

        This function creates and launches a Playwright synchronous browser.

        :param headless: Whether to launch the browser in headless mode. Default is True.
        :type handless: bool, optional
        :return: The created Playwright synchronous browser instance.
        :rtype: SyncBrowser




