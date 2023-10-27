from typing import Dict, Type, Union

from datapipes.datapipe_types import DatapipeType
from datapipes.datapipe import DataPipe
from datapipes.memory import Memory


DATAPIPE_TO_CLASS: Dict[DatapipeType, Type[DataPipe]] = {
  DatapipeType.MEMORY: Memory
}
