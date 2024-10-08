from typing import Dict
from typing import Type

from datapipe import DataPipe
from datapipe_types import DatapipeType
from memory import Memory


DATAPIPE_TO_CLASS: Dict[DatapipeType, Type[DataPipe]] = {
    DatapipeType.MEMORY: Memory
}
