from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from abc import abstractmethod
from pydantic import BaseModel


class BaseLLM(BaseModel):
    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @abstractmethod
    def generate(
            self,
            query: str,
            **kwargs: Any
    ) -> str:
        """
        This is an abstract method that should be implemented by subclasses.
        It should call the selected LLM and generate a response based on the provided query and any additional keyword arguments.
        The specific implementation may vary depending on the subclass.

        Args:
            self (object): The instance of the class.
            query (str): The query for generating the response.
            **kwargs (Any): Additional keyword arguments that may be required by subclasses.
        Return:
            str: The generated response.


        """
