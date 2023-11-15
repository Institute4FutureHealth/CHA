from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from datapipes.datapipe import DataPipe
from datapipes.types import DATAPIPE_TO_CLASS


def initialize_datapipe(
        datapipe: str = "memroy",
        **kwargs: Any
) -> DataPipe:
    """
    Initialize and return an instance of a data pipe based on the specified 'datapipe' type.

    Args:
        datapipe (str , optional): A string specifying the type of data pipe to initialize (default is "memory").
        kwargs (Any): Optional keyword arguments to be passed to the data pipe constructor.
    Return:
        DataPipe: An instance of the selected data pipe class.
    Raise:
        ValueError: If the specified 'datapipe' type is not valid, with a message listing valid types.



    Example:
        .. code-block:: python

            from langchain import ReActChain, OpenAI
            react = ReAct(llm=OpenAI())

    """

    if datapipe not in DATAPIPE_TO_CLASS:
        raise ValueError(
            f"Got unknown planner type: {datapipe}. "
            f"Valid types are: {DATAPIPE_TO_CLASS.keys()}."
        )

    datapipe_cls = DATAPIPE_TO_CLASS[datapipe]
    datapipe = datapipe_cls()
    return datapipe
