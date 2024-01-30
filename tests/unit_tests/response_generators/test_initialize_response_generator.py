from src.llms import LLMType
from src.response_generators import (
    initialize_response_generator,
)
from src.response_generators.response_generator import (
    BaseResponseGenerator,
)
from src.response_generators.response_generator_types import (
    ResponseGeneratorType,
)


def test_initialize_response_generator():
    llm_type = LLMType.OPENAI
    response_generator_type = ResponseGeneratorType.BASE_GENERATOR
    prefix = "Test Prefix"

    result = initialize_response_generator(
        llm=llm_type,
        response_generator=response_generator_type,
        prefix=prefix,
    )

    assert isinstance(result, BaseResponseGenerator)
