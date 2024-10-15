import os

import pytest

from llms import OpenAILLM


@pytest.fixture
def openai_llm(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", os.environ["OPENAI_API_KEY"])
    return OpenAILLM()


def test_is_max_token(openai_llm):
    model_name = "gpt-3.5-turbo"
    query = "your_query_here"
    result = openai_llm.is_max_token(model_name, query)
    assert isinstance(result, bool)


def test_get_model_names(openai_llm):
    model_names = openai_llm.get_model_names()
    assert isinstance(list(model_names), list)
    assert "gpt-3.5-turbo" in model_names


# def test_parse_response(openai_llm):
#     response_object = {"choices": [{"message": {"content": "generated_completion_text"}}]}
#     result = openai_llm._parse_response(response_object)
#     assert result == "generated_completion_text"
