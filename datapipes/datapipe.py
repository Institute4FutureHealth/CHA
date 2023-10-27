from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from abc import abstractmethod

class DataPipe():

  @abstractmethod
  def store(self, data):
    """
    """
  
  @abstractmethod
  def retrieve(self, key):
    """
    """ 