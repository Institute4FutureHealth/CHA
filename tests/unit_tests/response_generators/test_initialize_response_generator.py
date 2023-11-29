import os
from unittest.mock import patch
from llms.llm import BaseLLM
from llms.llm_types import LLMType
from response_generators.initialize_response_generator import initialize_response_generator
from response_generators.response_generator import BaseResponseGenerator
from response_generators.response_generator_types import ResponseGeneratorType


os.environ["OPENAI_API_KEY"] = "test key for openai"


def test_initialize_response_generator():
    llm_type = LLMType.OPENAI
    response_generator_type = ResponseGeneratorType.BASE_GENERATOR
    prefix = 'Test Prefix'

    result = initialize_response_generator(llm=llm_type, response_generator=response_generator_type, prefix=prefix)

    assert isinstance(result, BaseResponseGenerator)
