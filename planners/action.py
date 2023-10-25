from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

class Action:
  tool: str
  tool_input: Union[str, dict]
  log: str

