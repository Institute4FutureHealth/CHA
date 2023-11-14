Current package
===============





This code defines a class named CurrentWebPage that inherits from the BaseBrowser class. 
The CurrentWebPage class represents a task related to browser interactions, specifically retrieving the URL of the current web page.



- ``execute`` : This method executes the task by retrieving the current page from the synchronous browser using 
  the get_current_page function and returning its URL.

    .. py:function:: execute(self, input: str)

        Execute the current_page task by retrieving the URL of the current web page.

        :param input: The input string (not used in this task).
        :type input: str
        :return: The URL of the current web page.
        :rtype: str
        :raise ValueError: If the synchronous browser is not provided.


|


- ``explain`` : This method provides a brief explanation of the task.

    .. py:function:: explain(self)

        Provide a brief explanation of the current_page task.

        :return: An explanation of the task.
        :rtype: str



