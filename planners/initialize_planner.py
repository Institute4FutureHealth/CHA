from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from tasks.task import BaseTask
from llms.llm import BaseLLM
from planners import PLANNER_TO_CLASS

def initialize_planner(
  tasks: List[BaseTask],
  llm: BaseLLM,
  planner: str = "zero-shot-react-planner",
  **kwargs: Any
):

  if planner not in PLANNER_TO_CLASS:
    raise ValueError(
      f"Got unknown planner type: {planner}. "
      f"Valid types are: {PLANNER_TO_CLASS.keys()}."
    )
    
  planner_cls = PLANNER_TO_CLASS[planner]
  planner = planner_cls(llm_model=llm, available_tasks=tasks)
  return planner