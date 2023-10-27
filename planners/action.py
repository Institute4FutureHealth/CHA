from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

class Action:
  task: str
  task_input: str
  log: str

class PlanFinish:
  response: dict 
  log: str