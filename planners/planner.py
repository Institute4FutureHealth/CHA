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
    return "\n".join([f"[{task.get_dict()}]" for task in self.available_tasks])

  def get_available_tasks_list(self) -> List[str]:
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
      
      """

  @abstractmethod
  def parse(
        self,
        query: str,
        **kwargs: Any,
      ) -> List[Action]:
      """
      
      """