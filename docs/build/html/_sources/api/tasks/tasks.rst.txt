Tasks
=====




This class defines a base class named BaseTask. This class serves as a foundation for defining common properties 
and behaviors among various tasks in the system.


- ``execute``: An abstract method representing the execution of the task. Subclasses must implement this method.

    .. py:function:: execute(self, input: str)

        Abstract method representing the execution of the task.

        :param input: Input data for the task.
        :type input: str
        :return: Result of the task execution.
        :rtype: str
        :rise NotImplementedError: Subclasses must implement the execute method.


|



- ``parse_input`` : Parses the input string into a list of strings.

    .. py:function:: parse_input(self, input: str)

        Parse the input string into a list of strings.

        :param input: Input string to be parsed.
        :type input: str
        :return: List of parsed strings.
        :rtype: List[str]



|


- ``get_dict`` : Generates a dictionary-like representation of the task with details about its name, description, inputs, and dependencies.

    .. py:function:: get_dict(self)

        Generate a dictionary-like representation of the task.

        :return: String representation of the task dictionary.
        :rtype: str


|


- ``explain`` : Provides a sample explanation for the task.

    .. py:function:: explain(self)

        Provide a sample explanation for the task.

        :return: Sample explanation for the task.
        :rtype: str




