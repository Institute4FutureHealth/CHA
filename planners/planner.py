from __future__ import annotations

from abc import abstractmethod
from typing import Any
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel

from llms.llm import BaseLLM
from planners.action import Action
from planners.action import PlanFinish
from tasks.task import BaseTask


class BasePlanner(BaseModel):
    """
    **Description:**

        This class is the base implementation for the Planner. For every new planner that you want to create, you should
        inherit from this class and override the attributes and methods based on your planner's need.
        For sample implementaion look at `ReAct Implementation <_modules/planners/react.html#ReActPlanner>`_

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
        outputs:        This is the list of the description of the outputs that the task returns. This helps the planner to understand the returned
                        results better and use it as needed. For example, if the task returns a list of sleep hours for different sleep states,
                        the description helps planner learn which number is related to what state.
        output_type:    This indicates if the task result should be stored in the DataPipe or be returned directly to the planner.
                        This process will be done in the parse_input and post_execute methods. If needed you can overwrite them.
        return_direct:  This indicates if this task should completely interrupt the planning process or not.
                        This is needed in cases like when you want to ask a question from user and no further planning is
                        needed until the user gives the proper answer (look at ask_user task)
    """

    llm_model: BaseLLM = None
    available_tasks: Optional[List[BaseTask]] = []
    use_previous_action: bool = False

    @property
    def _planner_type(self):
        raise NotImplementedError

    @property
    def _planner_model(self):
        return self.llm_model

    @property
    def _stop(self) -> List[str]:
        return None

    @property
    def _planner_prompt(self):
        return """
        Sample prompt
        """

    def get_available_tasks(self) -> str:
        """
            Get a string formatted representation of available tasks.

        Return:
            str: Formatted string of available tasks.

        """

        return "\n".join(
            [
                f"\n-----------------------------------\n{task.get_dict()}\n-----------------------------------\n"
                for task in self.available_tasks
            ]
        )

    def get_available_tasks_list(self) -> List[str]:
        """
            Returns a list of names of available tasks.

        Return:
            List[str]: List of task names.

        """
        return [task.name for task in self.available_tasks]

    def self_reflect(self, user_query, final_answer):
        print(
            "self reflect",
            (
                "Based on the user_query, is the final_answer good or accurate Yes/No?\n"
                f"user_query: {user_query}\n"
                f"final_answer: {final_answer}"
            ),
        )
        answer = self._planner_model.generate(
            (
                "Based on the user_query, is the final_answer good or accurate Yes/No and explain why?\n"
                f"user_query: {user_query}\n"
                f"final_answer: {final_answer}"
            )
        )
        return answer

    @abstractmethod
    def plan(
        self,
        query: str,
        history: str,
        meta: str,
        previous_actions: List[Action] = None,
        use_history: bool = False,
        **kwargs: Any,
    ) -> List[Union[Action, PlanFinish]]:
        """
            Abstract method for generating a plan based on the input query and history.

        Args:
            query (str): Input query.
            history (str): History information.
            meta (str): meta information.
            previous_actions (List[Action]): List of previous actions.
            use_history (bool): Flag indicating whether to use history.
            **kwargs (Any): Additional keyword arguments.
        Return:
            List[Union[Action, PlanFinish]]: List of planned actions or finishing signals.

        """

    @abstractmethod
    def parse(
        self,
        query: str,
        **kwargs: Any,
    ) -> List[Union[Action, PlanFinish]]:
        """
            Abstract method for parsing the planner output into actions or a final answer.

        Args:
            query (str): Input query.
            **kwargs (Any): Additional keyword arguments.
        Return:
            Union[Action, PlanFinish]: List of parsed actions or finished plan.

        """
