from __future__ import annotations
from abc import abstractmethod
from typing import List, Optional
from pydantic import BaseModel


class BaseTask(BaseModel):
    """
    A brief description of MyClass.

    Attributes:
        name: The name of the task. It should be unique underscore_case to be defined in TaskType. sample_task_name
        chat_name: This is the name that later will be used if needed to mention the tasks inside the chat with the user. It should be Camel Case. SampleTaskChatName
        description: The description of the what specifically the task is doing. Try to define it as specific as possible to help the Task Planner decide better.
        dependencies: You can put the name of the TaskTypes that this task is dependent on. For example, in stress detection scenario, the stress analysis is dependent on the fetch hrv data task. [TaskType.SERPAPI, TASKTYPE.EXTRACT_TEXT]
        inputs: This is the list of descriptions for the inputs that should be provided by the planner. For example if your task has two inputs: ["the first input description", "the second input description"]
        outputs: This is the list of the description of the outputs that the task returns. This helps the planner to understand the returned results better and use it as needed. For example, if the task returns a list of sleep hours for different sleep states, the description helps planner learn which number is related to what state. 
        output_type: This indicates if the task result should be stored in the DataPipe or be returned directly to the planner. This process will be done in the parse_input and post_execute methods. If needed you can overwrite them.
        return_direct: This indicates if this task should completely interrupt the planning process or not. This is needed in cases like when you want to ask a question from user and no further planning is needed until the user gives the proper answer (look at ask_user task)
    """
    name: str
    chat_name: str
    description: str
    dependencies: List[str] = []
    inputs: List[str] = []
    outputs: List[str] = []
    # False if the output should directly passed back to the planner.
    # True if it should be stored in datapipe
    output_type: bool = False
    # False if planner should continue. True if after this task the planning should be
    # on pause or stop. examples are when you have a task that asks user to provide more information
    return_direct: bool = False

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        super().__init__()

    @property
    def name(self):
        return self.name

    @property
    def dependencies(self):
        return self.dependencies

    @property
    def inputs(self):
        return ", ".join([f"{str(i)}-{input}" for i, input in enumerate(self.inputs)])

    @abstractmethod
    def execute(
        self,
        input: str,
      ) -> str:
        """
            Abstract method representing the execution of the task.

            Args:
                input Input data for the task.
            Return:
                str: Result of the task execution.
            Raise:
                NotImplementedError: Subclasses must implement the execute method.

        """

    def parse_input(
        self,
        input: str,
      ) -> List[str]:
        """
            Parse the input string into a list of strings.

            Args:
                input Input string to be parsed.
            Return:
                List[str]: List of parsed strings.


        """  
        inputs = input.split(",")
        return [arg.strip() for arg in inputs]

    def get_dict(self) -> str:
        """
        Generate a dictionary-like representation of the task.

        Return:
            str: String representation of the task dictionary.


        """

        inputs = ",".join(self.inputs)
        dependencies = ",".join(self.dependencies)
        prompt = f"tool name:{self.name}, description: {self.description}."
        if len(self.inputs) > 0:
            prompt += f"The input to this tool should be comma separated list of data representing: {inputs}"
        if len(self.dependencies) > 0:
            prompt += f"\nThis tool is dependent on the following tools. make sure these tools are called first: '{dependencies}'"
        # prompt += "\n"
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
