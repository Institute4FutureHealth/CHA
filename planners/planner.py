from __future__ import annotations
from abc import abstractmethod
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from planners.action import Action
from tasks.task import BaseTask
from llms.llm import BaseLLM

class BasePlanner():
  """Base Planner class."""
  llm_model: BaseLLM = None
  available_tasks: Optional[List[BaseTask]] = []

  def __init__(self, llm_model, available_tasks):
    self.llm_model = llm_model
    self.available_tasks = available_tasks

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

  @abstractmethod
  def plan(
        self,
        query: str,
        history: str,
        previous_actions: List[Action],
        use_history: bool = False,
        **kwargs: Any,
      ) -> List[Action]:
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