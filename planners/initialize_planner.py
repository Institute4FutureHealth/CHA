from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from tasks.task import BaseTask
from llms.llm import BaseLLM
from planners.planner import BasePlanner
from planners.types import PLANNER_TO_CLASS
from llms.types import LLM_TO_CLASS

def initialize_planner(
  tasks: List[BaseTask],
  llm: str="openai",
  planner: str = "zero-shot-react-planner",
  **kwargs: Any
) -> BasePlanner:

  if planner not in PLANNER_TO_CLASS:
    raise ValueError(
      f"Got unknown planner type: {planner}. "
      f"Valid types are: {PLANNER_TO_CLASS.keys()}."
    )

  if llm not in LLM_TO_CLASS:
    raise ValueError(
      f"Got unknown llm type: {llm}. "
      f"Valid types are: {LLM_TO_CLASS.keys()}."
    )
  
  planner_cls = PLANNER_TO_CLASS[planner]
  llm_model = LLM_TO_CLASS[llm]()
  planner = planner_cls(llm_model=llm_model, available_tasks=tasks)
  return planner