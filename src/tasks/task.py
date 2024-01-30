from __future__ import annotations

import json
import re
from abc import abstractmethod
from typing import Any
from typing import List

from pydantic import BaseModel

from datapipes.datapipe import DataPipe


class BaseTask(BaseModel):
    """
    **Description:**

        This class is the base implementation for the Tasks. For every new task that you want to create, you should
        inherit from this class and override the attributes and methods based on your task's need. This class defines a base class named BaseTask.
        This class serves as a foundation for defining common properties and behaviors among various tasks in the system.

    Attributes:
        name:           The name of the task. It should be unique underscore_case to be defined in TaskType. sample_task_name
        chat_name:      This is the name that later will be used if needed to mention the tasks inside the chat with the user.
                        It should be Camel Case. SampleTaskChatName
        description:    The description of the what specifically the task is doing.
                        Try to define it as specific as possible to help the Task Planner decide better.
        dependencies:   You can put the name of the TaskTypes that this task is dependent on. For example, in stress detection scenario,
                        the stress analysis is dependent on the fetch hrv data task. [TaskType.SERPAPI, TASKTYPE.EXTRACT_TEXT]
        inputs:         This is the list of descriptions for the inputs that should be provided by the planner.
                        For example if your task has two inputs: ["the first input description", "the second input description"]
        outputs:        This is the list of the description of the outputs that the task returns.
                        This helps the planner to understand the returned results better and use it as needed.
                        For example, if the task returns a list of sleep hours for different sleep states,
                        the description helps planner learn which number is related to what state.
        output_type:    This indicates if the task result should be stored in the DataPipe or be returned directly to the planner.
                        This process will be done in the parse_input and post_execute methods. If needed you can overwrite them.
        return_direct:  This indicates if this task should completely interrupt the planning process or not.
                        This is needed in cases like when you want to ask a question from user and no further
                        planning is needed until the user gives the proper answer (look at ask_user task)
    """

    name: str
    chat_name: str
    description: str
    dependencies: List[str] = []
    inputs: List[str] = []
    outputs: List[str] = []
    datapipe: DataPipe = None
    # False if the output should directly passed back to the planner.
    # True if it should be stored in datapipe
    output_type: bool = False
    # False if planner should continue. True if after this task the planning should be
    # on pause or stop. examples are when you have a task that asks user to provide more information
    return_direct: bool = False

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    @property
    def name(self):
        return self.name

    @property
    def dependencies(self):
        return self.dependencies

    @property
    def inputs(self):
        return ", ".join(
            [
                f"{str(i)}-{input}"
                for i, input in enumerate(self.inputs)
            ]
        )

    @abstractmethod
    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        """
            Abstract method representing the execution of the task. You should implement this method based on your need.
            This method is called by the **execute** method that provides the parsed inputs to this method.

        Args:
            inputs (List[Any]): Input data for the task.
        Return:
            str: Result of the task execution.
        Raise:
            NotImplementedError: Subclasses must implement the execute method.

        """

    def _parse_input(
        self,
        input_args: List[str],
    ) -> List[str]:
        """
            Parses the input string into a list of strings. If the input is in format `datapipe:key`,
            the parser will retrieve the data from datapipe before sending it over to the **_execute** method.

        Args:
            input_args List(str): List of Input string provided by planner. It should be parsed and return a list of str variables.
        Return:
            List[str]: List of parsed strings. These strings can be converted into desired types inside **_execute** method.


        """
        return [
            json.loads(
                self.datapipe.retrieve(
                    re.search(r"datapipe:[0-9a-f\-]{36}", arg)
                    .group()
                    .strip()
                    .split(":")[-1]
                )
            )
            if "datapipe" in arg
            else arg.strip()
            for arg in input_args
        ]

    def _validate_inputs(self, inputs: List[str]) -> bool:
        """
            This method is called inside **execute** method after calling **_parse_input**. The result of **_parse_input** will be passed to this
            method to check the validity of the provided inputs by the Task Planner. Currently it only checks the length of the parsed input and
            the length of the inputs attribute of the tasks class. You can inherit this function to further add more input checkings for your own
            tasks.

        Args:
            inputs (List): List of strings containig the parsed inputs.
        Return:
            bool: True if the inputs are valid, False otherwise

        """
        valid = True
        if len(inputs) != len(self.inputs):
            valid = False
        return valid

    def _post_execute(self, result: str = "") -> str:
        """
            This method is called inside **execute** method after calling **_execute**. The result of **_execute** will be passed to this method
            in case the **output_type** attribute is True, the result will be stored inside the datapipe and the datapipe key is returned to
            the plenner instead of the raw result. This is good practice for times that you have intermediate data (like sleep data over a month)
            and it needs to be passed over to other tasks and the raw result is not immidiately needed.
            This will save a huge amount of tokens and makes sure that the planner will not pass wrong raw data to the tasks.

            It is important to note that to make the **DataPipe's** stored data standard and unified, we store the data in the json string
            format that currently contains 'data' and 'description' keys. The 'data' will be the returned data after execution and the 'description'
            is created using the **outputs** attribute of the task. Whenever the raw data is returned to the planner, these **outputs** descriptions
            will help the planner understand and learn how to interpret the 'data' to generate the final answer or continue planning.

        Args:
            result (str): string containig the task result.
        Return:
            List[str]: List of parsed strings.

        """
        if self.output_type:
            key = self.datapipe.store(
                json.dumps(
                    {
                        "data": result,
                        "description": "\n".join(self.outputs),
                    }
                )
            )
            return f"datapipe:{key}"
        return result

    def _get_input_format(self):
        return "\n".join(
            f"  {i+1}-{word}\n" for i, word in enumerate(self.inputs)
        )

    def execute(self, input_args: List[str]) -> str:
        """
            This method is called by the **Orchestrator** which provides the planner provided inputs.
            This method first calls **_parse_input** to parse the inputs and retrieve needed data from the **DataPipe**
            Then **_execute** is called and the parsed inputs are given to this method. Finally the final result of execution is passed to
            **_post_execute** and ith will either be stored inside **DataPipe** or directly returned to the planner to continue planning.

        Args:
            input_args (str): Input string provided by planner.
        Return:
            str: The final result of the task execution.

        """
        inputs = self._parse_input(input_args)
        if not self._validate_inputs(inputs):
            inputs_format = self._get_input_format()
            raise ValueError(
                "Wrong inputs are provided."
                f"The inputs should follow the descriptions: {inputs_format}"
            )
        result = self._execute(inputs)
        return self._post_execute(result)

    def get_dict(self) -> str:
        """
            Generate a dictionary-like representation of the task.

        Return:
            str: String representation of the task dictionary.


        """
        dependencies = ",".join(
            f"{i+1}-{word}"
            for i, word in enumerate(self.dependencies)
        )
        prompt = f"**{self.name}**: {self.description}"
        if len(self.inputs) > 0:
            inputs = self._get_input_format()
            prompt += f"\n  The input to this tool should be a list of data representing:\n {inputs}"
        if len(self.dependencies) > 0:
            prompt += f"\n  This tool is dependent on the following tools. make sure these tools are called first: {dependencies}"
        if len(self.outputs) > 0:
            prompt += (
                "\n   This tool will return the following data:\n- "
                + "\n- ".join(self.outputs)
            )
        if self.output_type:
            prompt += "\n The result will be stored in datapipe."
        return prompt

    def explain(
        self,
    ) -> str:
        """
            Provide a sample explanation for the task.

        Return:
            str: Sample explanation for the task.


        """

        return """
        Sample Explanation
        """
