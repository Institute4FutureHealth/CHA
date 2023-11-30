from typing import Any

from llms.llm import BaseLLM
from llms.llm_types import LLMType
from llms.types import LLM_TO_CLASS
from response_generators.response_generator import (
    BaseResponseGenerator,
)
from response_generators.response_generator_types import (
    ResponseGeneratorType,
)
from response_generators.types import RESPONSE_GENERATOR_TO_CLASS


def initialize_response_generator(
    llm: str = LLMType.OPENAI,
    response_generator: str = ResponseGeneratorType.BASE_GENERATOR,
    prefix: str = "",
    **kwargs: Any,
) -> BaseResponseGenerator:
    """
    This method provides a convenient way to initialize a response generator based on the specified language model type
    and response generator type. It handles the instantiation of the language model and the response generator class.

    Args:
        llm (str): Type of language model type to be used.
        response_generator (str): Type of response generator to be initialized.
        prefix (str): Prefix to be added to generated responses.
        **kwargs (Any): Additional keyword arguments.
    Return:
        BaseResponseGenerator: Initialized instance of the response generator.



    Example:
        .. code-block:: python

            from llms.llm_types import LLMType
            from response_generators.response_generator_types import ResponseGeneratorType
            response_generators = initialize_planner(llm=LLMType.OPENAI, response_generator=ResponseGeneratorType.BASE_GENERATOR)

    """

    if response_generator not in RESPONSE_GENERATOR_TO_CLASS:
        raise ValueError(
            f"Got unknown planner type: {response_generator}. "
            f"Valid types are: {RESPONSE_GENERATOR_TO_CLASS.keys()}."
        )

    if llm not in LLM_TO_CLASS:
        raise ValueError(
            f"Got unknown llm type: {llm}. "
            f"Valid types are: {LLM_TO_CLASS.keys()}."
        )

    response_generator_cls = RESPONSE_GENERATOR_TO_CLASS[
        response_generator
    ]
    llm_model = LLM_TO_CLASS[llm]()
    response_generator = response_generator_cls(
        llm_model=llm_model, prefix=prefix
    )
    return response_generator
