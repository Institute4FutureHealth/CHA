from __future__ import annotations
from abc import abstractmethod
from typing import Any, List, Optional, Union
from planners.action import Action, PlanFinish
from tasks.task import BaseTask
from llms.llm import BaseLLM
from pydantic import BaseModel


class BasePlanner(BaseModel):
    """Base Planner class."""
    llm_model: BaseLLM = None
    available_tasks: Optional[List[BaseTask]] = []

    @property
    def _planner_type(self):
        raise NotImplemented

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

        return "\n".join([f"[{task.get_dict()}]" for task in self.available_tasks])

    def get_available_tasks_list(self) -> List[str]:
        """
        Returns a list of names of available tasks.

        Return:
            List[str]: List of task names.

        """

        return [task.name for task in self.available_tasks]

    @abstractmethod
    def plan(
            self,
            query: str,
            history: str,
            meta: str,
            previous_actions: List[Action],
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
