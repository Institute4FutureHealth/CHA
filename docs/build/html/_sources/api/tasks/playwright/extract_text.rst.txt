Extract Text
============





This task extracts all the text from the current webpage.


- ``check_bs_import_lxml_import`` : Check that the 'beautifulsoup4' and 'lxml' packages are installed.

    .. py:function:: check_bs_import_lxml_import(cls, values: dict)

        Check that the 'beautifulsoup4' and 'lxml' packages are installed.

        :param values: The current attribute values.
        :type values: dict
        :raise ImportError: If 'beautifulsoup4' or 'lxml' packages are not installed.
        :return: The updated attribute values.
        :rtype: dict


|


- ``execute`` : Execute the ExtractText task.

    .. py:function:: execute(self, input: str)

        Execute the ExtractText task.

        :param input: The input parameter for the task.
        :type input: str
        :raise ValueError: If the synchronous browser is not provided.
        :return: The extracted text from the current webpage.
        :rtype: str


|


- ``explain`` : Explain the ExtractText task.

    .. py:function:: explain(self)

        Explain the ExtractText task.

        :return: A brief explanation of the ExtractText task.
        :rtype: str






