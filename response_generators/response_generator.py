from __future__ import annotations
from abc import abstractmethod
from typing import Any, List

from llms.llm import BaseLLM

class BaseResponseGenerator():
  """Base Response Generator class."""
  llm_model: BaseLLM = None
  prefix: str = ""

  @property
  def _response_generator_type(self):
    raise NotImplemented

  @property
  def _response_generator_model(self):
    return None

  @abstractmethod
  def generate(
        self,
        query: str,
        **kwargs: Any,
      ) -> List[str]:
    """
    
    """