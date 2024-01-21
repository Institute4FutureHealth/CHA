import re
import traceback
from typing import Any
from typing import Dict
from typing import List

from pydantic import model_validator

from llms.initialize_llm import initialize_llm
from llms.llm import BaseLLM
from llms.llm_types import LLMType
from tasks.task import BaseTask


class RunPythonCode(BaseTask):
    """
    **Description:**

        This task is recieves a description and the needed data and asks an LLM to generate a python code to solve the problem
        stated in the description. Then it runs the python code and returns the result.

    """

    name: str = "run_python_code"
    chat_name: str = "RunPythonCode"
    description: str = (
        "This tool should be used to convert data formats, plot data, or perform basic "
        "statistical tasks like mean, and sum."
    )
    dependencies: List[str] = []
    inputs: List[str] = [
        "You should provide the data source, which is in form of datapipe:datapipe_key",
        "You should provide a descriptive Chain of Thought prompt to help this tool solve the problem the "
        "best way possible.",
    ]
    outputs: List[str] = []
    output_type: bool = False
    llm_model: BaseLLM = None
    max_retrie: int = 3

    @model_validator(mode="before")
    def validate_environment(cls, values: Dict) -> Dict:
        """
            Validate that api key and python package exists in environment.

        Args:
            values (Dict): The dictionary of attribute values.
        Return:
            Dict: The updated dictionary of attribute values.
        Raise:
            ValueError: If the SerpAPI python package is not installed.

        """

        values["llm_model"] = initialize_llm(LLMType.OPENAI)
        return values

    def _generate_prompt(self, previous_attempts, inputs):
        prompt = (
            "Assume that the input data contains the following keys:"
            f"\n\n{inputs[0]['description']}\n\n"
            "If the final result is a plot, or image, you SHOULD save them inside the 'data' folder with a random uuid "
            "name and suffix and return the final path in the following format: `address:[path]`. "
            "Otherwise simply return the data itself."
            "Only return the code. Make sure you IMPORT ALL necessary libraries."
            "Priorities provided keys over the problem statement for choosing the right keys. Ignore keys that does not exist."
            "In custom_function, always check if the input is json or json string and convert it to json if needed."
        )
        if len(previous_attempts) > 0:
            prompt = (
                f"Previous Attempt: {previous_attempts}\n\n"
                "Considering the Previous Attempt and errors, fix the python code"
                f"to solve the following problem:\n{inputs[1]}\n\n"
            ) + prompt
        else:
            prompt = (
                "Generate a python code which contains a function named 'custom_function' with one "
                f"json input to solve the following problem:\n\n{inputs[1]}\n\n"
            ) + prompt
        prompt = (
            "You are skilled python programmer that can solve problems and convert them into python codes."
            + prompt
        )
        return prompt

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        """Translate query"""
        previous_attempts = ""
        retries = 0
        while retries < self.max_retrie:
            try:
                prompt = self._generate_prompt(
                    previous_attempts, inputs
                )

                print("code prompt: ", prompt)
                kwargs = {"max_tokens": 1000}
                code = self.llm_model.generate(prompt, **kwargs)
                previous_attempts = f"\n{code}"
                pattern = r"```python\n(.*?)```"
                code = re.search(pattern, code, re.DOTALL).group(1)
                print("generated code", code)
                global result
                result = ""
                code += (
                    f"\nresult=custom_function({inputs[0]['data']})"
                )
                exec(code, locals())
                result = locals().get("result")
                print("result", result)
                return result
            except Exception:
                retries += 1
                previous_attempts += (
                    f"\nError:{traceback.format_exc()}"
                )
        raise ValueError("Error running code")

    def explain(
        self,
    ) -> str:
        return "This task simply asks user to provide more information or continue interaction."
