from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from abc import abstractmethod

class BaseLLM():
  @abstractmethod
  def generate(
        self,
        query: str,
        **kwargs: Any
      ) -> str: 
      """
      """