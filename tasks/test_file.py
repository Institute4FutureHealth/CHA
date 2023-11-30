from typing import Any
from typing import List

from tasks.task import BaseTask


class TestFile(BaseTask):
    name: str = "test_file"
    chat_name: str = "TestFile"
    description: str = "analyzes the image and returns description."
    dependencies: List[str] = []
    inputs: List[str] = ["the image file name"]
    outputs: List[str] = []
    output_type: bool = False
    return_direct: bool = True

    translator: Any = None  #: :meta private:

    def parse_input(
        self,
        input: str,
    ) -> List[str]:
        """
        Parse the input string into a list of strings.

        Args:
            input (str): Input string to be parsed.
        Return:
            List[str]: List of parsed strings.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        return input.split("$#")

    def execute(
        self,
        input: str,
    ) -> str:
        """
        Abstract method representing the execution of the task.

        Args:
            input (str): Input data for the task.
        Return:
            str: Result of the task execution.
        Raise:
            NotImplementedError: Subclasses must implement the execute method.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        self.parse_input(input)
        return "this image is a classification results of a data"

    def explain(
        self,
    ) -> str:
        """
        Provide a sample explanation for the task.

        Return:
            str: Sample explanation for the task.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        return "This task simply asks user to provide more information or continue interaction."
