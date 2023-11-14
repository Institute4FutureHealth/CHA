Get Elements
============





The GetElements class is a subclass of BaseBrowser responsible for retrieving elements 
on the current web page that match a given CSS selector.




- ``_get_elements`` : Get elements matching the given CSS selector.

    .. py:function:: _get_elements(page: SyncPage, selector: str, attributes: Sequence[str])

        Get elements matching the given CSS selector.

        :param page: The current page.
        :type page: SyncPage 
        :param selector (str): CSS selector to match elements.
        :type selector: str
        :param attributes: Set of attributes to retrieve for each element.
        :type attributes: Sequence[str]
        :return: A list of dictionaries containing the retrieved elements and their attributes.
        :rtype: List[dict]


|


- ``execute`` : Execute the GetElements task.

    .. py:function:: execute(self, input: str)

        Execute the GetElements task.

        :param input: Input string containing CSS selector and attributes.
        :type input: str
        :raise ValueError: If the synchronous browser is not provided.
        :return: The JSON-formatted string containing the retrieved elements and their attributes.
        :rtype: str


|


- ``explain`` : Explain the GetElements task.

    .. py:function:: explain(self)

        Explain the GetElements task.

        :return: A brief explanation of the GetElements task.
        :rtype: str












