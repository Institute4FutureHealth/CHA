from typing import Dict
from typing import Type

from openCHA.datapipes import DataPipe
from openCHA.datapipes import DatapipeType
from openCHA.datapipes import Memory


DATAPIPE_TO_CLASS: Dict[DatapipeType, Type[DataPipe]] = {
    DatapipeType.MEMORY: Memory
}
