import uuid
from typing import Any
from typing import Dict
from typing import Optional

from datapipes.datapipe import DataPipe


class Memory(DataPipe):
    """
    **Description:**

        This class inherits from DataPipe and uses simple on memory python dictionary.
    """

    data: Optional[Dict[str, Dict]] = {}

    def store(self, data) -> str:
        """
            Stores data using a randomly generated key and returns the key.

            This method stores the provided data in the memory data dictionary using a generated key.
            The generated key is created using UUID (Universally Unique Identifier) ensuring having unique keys for multiple data stores.
            The stored data can later be accessed using this key.

        Args:
            self (object): The instance of the class.
            data (Any): The data to be stored.
        Return:
            str: The generated key associated with the stored data.



        Example:
            .. code-block:: python

                from datapipes.datapipe_types import DatapipeType
                memory = initialize_datapipe(datapipe=DatapipeType.MEMORY)
                key = memory.store("this is sample string to be stored")

        """

        key = str(uuid.uuid4())
        self.data[key] = data
        return key

    def retrieve(self, key) -> Any:
        """
            Retrieves stored data using the given key.

            This method retrieves the data associated with the provided key from the memory data dictionary.
            If the key does not exist in the dictionary, it raises a `ValueError` with an appropriate error message.

        Args:
            self (object): The instance of the class.
            key (str): The key associated with the data to be retrieved.
        Return:
            Any: The data associated with the provided key.
        Raise:
            ValueError: If the key does not exist in the data dictionary.



        Example:
            .. code-block:: python

                from datapipes.datapipe_types import DatapipeType
                memory = initialize_datapipe(datapipe=DatapipeType.MEMORY)
                memory.retrieve("UUID key returned from store")

        """

        if key not in self.data:
            raise ValueError(
                f"The data with the key {key} does not exist."
            )
        return self.data[key]
