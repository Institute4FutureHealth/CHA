from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from llms.llm import BaseLLM
from llms.types import LLM_TO_CLASS

def initialize_llm(
  llm: str = "openai",
  **kwargs: Any
) -> BaseLLM:

  if llm not in LLM_TO_CLASS:
    raise ValueError(
      f"Got unknown planner type: {llm}. "
      f"Valid types are: {LLM_TO_CLASS.keys()}."
    )
    
  llm_cls = LLM_TO_CLASS[llm]
  llm = llm_cls()
  return llm