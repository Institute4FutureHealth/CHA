Extract Hyperlinks
==================







This task extracts all hyperlinks from the current webpage.


- ``check_bs_import`` : Check that the 'beautifulsoup4' package is installed.

    .. py:function:: check_bs_import(cls, values: dict)

        Check that the 'beautifulsoup4' package is installed.

        :param values: The current attribute values.
        :type values: dict
        :raise ImportError: If 'beautifulsoup4' package is not installed.
        :return: The updated attribute values.
        :rtype: dict


|


- ``scrape_page`` : Scrape hyperlinks from the current webpage.

    .. py:function:: scrape_page(page: Any, html_content: str, absolute_urls: bool)

        Scrape hyperlinks from the current webpage.

        :param page: The current webpage.
        :type page: Any
        :param html_content: The HTML content of the webpage.
        :type html_content: str
        :param absolute_urls: True if absolute URLs should be returned, False otherwise.
        :type absolute_urls: bool
        :return: JSON string containing the extracted hyperlinks.
        :rtype: str


|


- ``execute`` : Execute the ExtractHyperlinks task.

    .. py:function:: execute(self, input: str)

        Execute the ExtractHyperlinks task.

        :param input: The input parameter for the task.
        :type input: str
        :raise ValueError: If the synchronous browser is not provided.
        :return: JSON string containing the extracted hyperlinks.
        :rtype: str


|


- ``explain`` : Provide a brief explanation of the ExtractHyperlinks task.

    .. py:function:: explain(self)

        Provide a brief explanation of the ExtractHyperlinks task.

        :return: An explanation of the task.
        :rtype: str



