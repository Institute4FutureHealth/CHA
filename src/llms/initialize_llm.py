from typing import Any

from llms.llm import BaseLLM
from llms.llm_types import LLMType
from llms.types import LLM_TO_CLASS


def initialize_llm(
    llm: str = LLMType.OPENAI, **kwargs: Any
) -> BaseLLM:
    """
    This function initializes and returns an instance of the Language Model Manager (LLM) based on the specified LLM type.

    Args:
        llm (str, optional): The LLM type to initialize. Defaults to "openai".
        **kwargs (Any, optional): Additional keyword arguments to pass to the LLM constructor.
    Return:
        BaseLLM: An instance of the initialized LLM.
    Raise:
        ValueError: If the specified LLM type is unknown.



    Example:
        .. code-block:: python

            from llms.llm_types import LLMType
            llm = initialize_llm(llm=LLMType.OPENAI)

    """

    if llm not in LLM_TO_CLASS:
        raise ValueError(
            f"Got unknown planner type: {llm}. "
            f"Valid types are: {LLM_TO_CLASS.keys()}."
        )

    llm_cls = LLM_TO_CLASS[llm]
    llm = llm_cls(**kwargs)
    return llm
