from __future__ import annotations
from abc import abstractmethod
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from action import Action

from llms.llm import BaseLLM

class BasePlanner():
  """Base Planner class."""
  llm_model: BaseLLM = None
  available_tools: Optional[List[str]] = []

  @property
  def _planner_type(self):
    raise NotImplemented

  @property
  def _planner_model(self):
    return None

  @property
  def _planner_prompt(self):
    return 
    """
    Sample prompt
    """

  def get_available_tasks(self) -> Optional[List[str]]:
    return self.available_tools

  @abstractmethod
  def plan(
        self,
        query: str,
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