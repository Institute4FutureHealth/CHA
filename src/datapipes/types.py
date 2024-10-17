from typing import Dict
from typing import Type

from datapipes import DataPipe
from datapipes import DatapipeType
from datapipes import Memory


DATAPIPE_TO_CLASS: Dict[DatapipeType, Type[DataPipe]] = {
    DatapipeType.MEMORY: Memory
}
