import json
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
        "This tool runs a python code based on the input query and returns the result. "
        "This tool should be used to convert data formats, plotting data, or performing basic "
        "statistical tasks like mean, and sum"
    )
    dependencies: List[str] = []
    inputs: List[str] = [
        "The description of what you want to be done.",
        "The needed data. You should pass the datapipe key not the raw data.",
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
            f"Generate a python function code named 'custom_function' with one json input to solve the following problem:\n{inputs[0]}\n"
            "The description of the json keys in the input data is as follows:"
            f"\n{inputs[1]['description']}\n\n"
            "If the final result is  plot, image, or any types of files, you SHOULD save them inside the 'data' folder with a random uuid "
            "name and suffix and return the final path in the following format: 'address:path'. "
            "If the data is raw data, simply return the data itself. Only return the code. Make sure you IMPORT ALL necessary libraries."
        )
        kwargs = {"max_tokens": 2000}
        code = self.llm_model.generate(prompt, **kwargs)
        pattern = r"```python\n(.*?)```"
        code = re.search(pattern, code, re.DOTALL).group(1)
        print("generated code", code)
        global result
        result = ""
        code += f"\nresult=custom_function({json.dumps(inputs[1]['data'])})"
        exec(code, locals())
        result = locals().get("result")
        if "address:" in result:
            self.output_type = False
            return result.split("address:")[-1]
        return result

    def explain(
        self,
    ) -> str:
        return "This task simply asks user to provide more information or continue interaction."
