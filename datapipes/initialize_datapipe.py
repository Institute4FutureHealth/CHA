from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from datapipes.datapipe import DataPipe
from datapipes.types import DATAPIPE_TO_CLASS

def initialize_datapipe(
  datapipe: str = "memroy",
  **kwargs: Any
) -> DataPipe:

  if datapipe not in DATAPIPE_TO_CLASS:
    raise ValueError(
      f"Got unknown planner type: {datapipe}. "
      f"Valid types are: {DATAPIPE_TO_CLASS.keys()}."
    )
    
  datapipe_cls = DATAPIPE_TO_CLASS[datapipe]
  datapipe = datapipe_cls()
  return datapipe