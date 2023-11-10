from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from abc import abstractmethod
from pydantic import BaseModel

class BaseLLM(BaseModel):
  class Config:
    """Configuration for this pydantic object."""
    arbitrary_types_allowed = True
    
  @abstractmethod
  def generate(
        self,
        query: str,
        **kwargs: Any
      ) -> str: 
      """
      """