from __future__ import annotations
from abc import abstractmethod
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

class Task():

  name: str
  chat_name: str
  description: str
  dependencies: List[str] = []
  inputs: List[str] = []
  outputs: List[str] = []
  output_type: bool = False


  @abstractmethod
  def execute(
        self,
        inputs: Optional[List[str]],

      ):
    """
    """

  def dict():
    return 

  def explain(
        self,
      ):
    return 
    """
      Sample Explanation
    """
