from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from abc import abstractmethod
from datapipes.datapipe import DataPipe
import uuid

class Memory(DataPipe):

    data: Optional[Dict[str, Dict]] = []

    def store(self, data) -> str:
        """
        Store data using a generated key and return the key.

        This method stores the provided data in the chatbot's data dictionary using a generated key.
        The generated key is a UUID (Universally Unique Identifier). The stored data can later be accessed using this key.

        Args:
            self (object): The instance of the class.
            data (Any): The data to be stored.
        Return:
            str: The generated key associated with the stored data.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """
        key = uuid.uuid4()
        self.data[key] = data
        return key

    def retrieve(self, key) -> Any:
        """
        Retrieve data associated with the given key.

        This method retrieves the data associated with the provided key from the chatbot's data dictionary.
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

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        if key not in self.data:
            raise ValueError(
                f"The data with the key {key} does not exist."
            )
        return self.data[key]
    