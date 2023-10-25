from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from abc import abstractmethod
from planners.planner import BasePlanner

class Orchestrator():
  
  planner: BasePlanner = None
  datapipe: Any = None
  promptist: Any = None 
  available_tasks: List[str]

  role: int = 0

  def process_meta(self):
    return False 
  
  def execute_task(self):
    return False

  def generate_prompt(self):
    return False 

  def generate_final_answer(self):
    return False

  def initialize_orchestrator(self):
    return self

  @abstractmethod
  def run(
        self,
        query: str,
        meta: Any,
        use_history: bool,
        **kwargs: Any
      ) -> str: 
      """
      """