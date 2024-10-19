from abc import abstractmethod
from typing import Any

from pydantic import BaseModel


class DataPipe(BaseModel):
    """
    **Description:**

        This class serves as a base class for creating new Data Pipes. Each new Data Pipe should implement the **store** and **retrieve** methods.
        The implementation should generate reasonable keys that can be used for accessing the data. It is recommended to not interfere in the way
        the data is stored. For example, changing the type of the data or the format of the data. If your Data Pipe requires specific format or
        type, make sure you the conversion inside the Data Pipe ensuring consistency in the way tasks interact with Data Pipes. Look at
        :ref:`memory` for sample implementation.
    """

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    @abstractmethod
    def store(self, data) -> str:
        """
            Storing intermediate results or needed information inside Data Pipe. This method should be implemented\
            in the class inheriting DataPipe.

        Args:
            data (Any): The data to be stored.
        Return:
            str: The name of the stored data.

        """

    @abstractmethod
    def retrieve(self, key) -> Any:
        """
            Retrieving data based on a key. The key is what is returned form `store`. This method should be implemented\
            in the class inheriting DataPipe.

        Args:
            key (Any): The key to identify the data.
        Return:
            Any: The retrieved data.

        """
