from llms import LLMType
from response_generators import (
    initialize_response_generator,
)
from response_generators import (
    BaseResponseGenerator,
)
from response_generators import (
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
