import os
from unittest.mock import MagicMock
import pytest
from llms.initialize_llm import initialize_llm
from llms.llm_types import LLMType
from llms.types import LLM_TO_CLASS


os.environ["OPENAI_API_KEY"] = "test key for openai"


def test_initialize_llm_valid_type():

    llm_type = LLMType.OPENAI
    llm_instance = initialize_llm(llm=llm_type)
    assert isinstance(llm_instance, LLM_TO_CLASS[llm_type])


def test_initialize_llm_invalid_type():

    with pytest.raises(ValueError):
        initialize_llm(llm='unknown_type')


def test_initialize_llm_with_kwargs():

    llm_type = LLMType.OPENAI
    kwargs = {'api_key': 'test key for openai'}
    llm_instance = initialize_llm(llm=llm_type, **kwargs)
    assert isinstance(llm_instance, LLM_TO_CLASS[llm_type])
    assert llm_instance.api_key == 'test key for openai'


def test_initialize_llm_with_mock():

    llm_type = LLMType.OPENAI
    mocked_llm_class = MagicMock()
    with pytest.MonkeyPatch().context() as m:
        m.setattr('llms.llm_manager.LLM_TO_CLASS', {llm_type: mocked_llm_class})
        llm_instance = initialize_llm(llm=llm_type)
    mocked_llm_class.assert_called_once()
    assert isinstance(llm_instance, mocked_llm_class)
