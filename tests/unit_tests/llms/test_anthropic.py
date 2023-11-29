import pytest
from unittest.mock import Mock
from llms.anthropic import AntropicLLM


@pytest.fixture
def anthropic_llm(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "your_api_key")
    return AntropicLLM()


def test_validate_environment(anthropic_llm):
    values = {"anthropic_api_key": "your_api_key"}
    result = anthropic_llm.validate_environment(values)
    assert "api_key" in result
    assert "llm_model" in result
    assert "HUMAN_PROMPT" in result
    assert "AI_PROMPT" in result


def test_get_model_names(anthropic_llm):
    model_names = anthropic_llm.get_model_names()
    assert isinstance(list(model_names), list)
    assert "claude-2" in model_names


@pytest.mark.asyncio
async def test_is_max_token(anthropic_llm):
    model_name = "claude-2"
    query = "your_query_here"
    result = await anthropic_llm.is_max_token(model_name, query)
    assert isinstance(result, bool)


def test_parse_response(anthropic_llm):
    response_object = {"completion": "generated_completion_text"}
    result = anthropic_llm._parse_response(response_object)
    assert result == "generated_completion_text"


def test_prepare_prompt(anthropic_llm):
    input_prompt = "user_input_prompt"
    result = anthropic_llm._prepare_prompt(input_prompt)
    assert isinstance(result, str)


def test_generate(anthropic_llm, monkeypatch):
    # Mocking the completions.create method to avoid actual API calls
    completions_mock = Mock()
    monkeypatch.setattr(anthropic_llm.llm_model(api_key=anthropic_llm.api_key), "completions.create", completions_mock)

    query = "your_query_here"
    result = anthropic_llm.generate(query)
    assert isinstance(result, str)
