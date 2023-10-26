from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

class Action:
  tool: str
  tool_input: str
  log: str
  finish: bool = False

class PlanFinish:
  response: dict 
  log: str