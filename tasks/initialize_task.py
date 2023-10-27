from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from tasks.task import BaseTask
from tasks.types import TASK_TO_CLASS

def initialize_task(
  task: str = "serpapi",
  **kwargs: Any
) -> BaseTask:

  if task not in TASK_TO_CLASS:
    raise ValueError(
      f"Got unknown planner type: {task}. "
      f"Valid types are: {TASK_TO_CLASS.keys()}."
    )
    
  task_cls = TASK_TO_CLASS[task]  
  task = task_cls()  
  return task