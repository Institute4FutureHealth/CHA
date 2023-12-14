import re
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
        "Data source - You should provide the data source, which is in form of "
        "datapipe:[datapipe_key] the datapipe_key should be extracted from the result of previous actions.",
        "Task description - You should provide a detailed description of the task you want to perform, NEVER provide codes. "
        "Be specific about what you want to achieve, such as plotting, data conversion, or statistical calculations."
        "You can use your Thought before action as input.",
    ]
    outputs: List[str] = []
    output_type: bool = False
    llm_model: BaseLLM = None

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

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        """Translate query"""
        prompt = (
            "Generate a python code which contains a function named 'custom_function' with one "
            f"json input to solve the following problem:\n{inputs[1]}\n"
            "The description of the json keys in the input data is as follows:"
            f"\n{inputs[0]['description']}\n\n"
            "If the final result is a plot, or image, you SHOULD save them inside the 'data' folder with a random uuid "
            "name and suffix and return the final path in the following format: 'address:path'. "
            "If the data is json or other numerical formats, simply return the data itself."
            "Only return the code. Make sure you IMPORT ALL necessary libraries."
            "Always make sure that you only use the keys which have the description. Always put checkings to see if specific key exists."
            "You can assume that the data contains enought information and does not rely on the keys that does not exist."
            "In custom_function, always check if the input is json or json string and convert it to json if needed."
        )
        kwargs = {"max_tokens": 1000}
        code = self.llm_model.generate(prompt, **kwargs)
        pattern = r"```python\n(.*?)```"
        code = re.search(pattern, code, re.DOTALL).group(1)
        print("generated code", code)
        global result
        result = ""
        code += f"\nresult=custom_function({inputs[0]['data']})"
        exec(code, locals())
        result = locals().get("result")
        print("result", result)
        if "address:" not in result:
            self.output_type = True
            return result
        return f"The code is successfully executed and the result is either stored as file path with address or returned directly. Result: {result}"

    def explain(
        self,
    ) -> str:
        return "This task simply asks user to provide more information or continue interaction."
