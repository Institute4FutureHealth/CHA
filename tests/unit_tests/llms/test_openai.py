import pytest
from unittest.mock import patch
from llms.openai import OpenAILLM


@pytest.fixture
def openai_llm(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "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")
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


def test_parse_response(openai_llm):
    response_object = {"choices": [{"message": {"content": "generated_completion_text"}}]}
    result = openai_llm._parse_response(response_object)
    assert result == "generated_completion_text"


@patch('llms.openai.OpenAILLM')
def test_generate(mock_openai, openai_llm):
    query = "your_query_here"
    mock_openai().chat.completions.create.return_value = {"choices": [{"message": {"content": "generated_response"}}]}
    result = openai_llm.generate(query)
    assert result == "generated_response"
