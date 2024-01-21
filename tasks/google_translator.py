"""
A part of the task implementation is borrowed from LangChain:
https://github.com/langchain-ai/langchain
"""
from typing import Any
from typing import Dict
from typing import List

from pydantic import model_validator

from tasks.task import BaseTask


class GoogleTranslate(BaseTask):
    """
    **Description:**

        This task uses google translate to autmatically convert from the user language to english or vise versa.

    """

    name: str = "google_translator"
    chat_name: str = "GoogleTranslator"
    description: str = (
        "Translates queries between different languages."
    )
    dependencies: List[str] = []
    inputs: List[str] = [
        "text to be translated",
        "destination language",
    ]
    outputs: List[str] = []
    output_type: bool = False

    translator: Any = None  #: :meta private:

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
            from googletrans import Translator

            values["translator"] = Translator()
        except ImportError:
            raise ValueError(
                "Could not import googletrans python package. "
                "Please install it with `pip install googletrans-py`."
            )
        return values

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        """
            Abstract method representing the execution of the task.

        Args:
            input (str): Input data for the task.
        Return:
            str: Result of the task execution.
        Raise:
            NotImplementedError: Subclasses must implement the execute method.

        """
        if len(inputs) < 2:
            return "", ""
        dest = inputs[1] if inputs[1] is not None else "en"
        result = self.translator.translate(inputs[0], dest=dest)
        return result.text, result.src

    def explain(
        self,
    ) -> str:
        """
            Provide a sample explanation for the task.

        Return:
            str: Sample explanation for the task.

        """

        return "This task uses google translate to translate between languages"
