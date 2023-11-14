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
      Store data in the system.

      :param data: The data to be stored.
      :type data: Any
      :return: The name of the stored data.
      :rtype: str

      """
  
  @abstractmethod
  def retrieve(self, key) -> Any:
    """
    """ 