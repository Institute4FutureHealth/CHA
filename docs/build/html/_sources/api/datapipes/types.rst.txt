Types
=====




Datapipe Types
--------------

This enumeration class defines different types of datapipe. 
It inherits from the `str` class and the `Enum` class in Python's `enum` module. 
Each value in this enumeration represents a specific type of datapipe.


.. code:: python

    from enum import Enum 

    class DatapipeType(str, Enum):
      MEMORY = "memory"


|


Types
-----


This dictionary is used to map each DatapipeType value to its corresponding DataPipe class. 
It allows for easy retrieval of the appropriate class based on the datapipe type.


.. code:: python

    from typing import Dict, Type, Union

    from datapipes.datapipe_types import DatapipeType
    from datapipes.datapipe import DataPipe
    from datapipes.memory import Memory
    
    DATAPIPE_TO_CLASS: Dict[DatapipeType, Type[DataPipe]] = {
      DatapipeType.MEMORY: Memory
    }







