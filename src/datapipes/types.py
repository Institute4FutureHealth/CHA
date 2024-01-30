from typing import Dict
from typing import Type

from datapipes.datapipe import DataPipe
from datapipes.datapipe_types import DatapipeType
from datapipes.memory import Memory


DATAPIPE_TO_CLASS: Dict[DatapipeType, Type[DataPipe]] = {
    DatapipeType.MEMORY: Memory
}
