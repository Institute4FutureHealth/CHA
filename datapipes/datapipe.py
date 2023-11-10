from typing import Any
from abc import abstractmethod
from pydantic import BaseModel

class DataPipe(BaseModel):

  class Config:
    """Configuration for this pydantic object."""
    arbitrary_types_allowed = True

  @abstractmethod
  def store(self, data) -> str:
    """
    """
  
  @abstractmethod
  def retrieve(self, key) -> Any:
    """
    """ 