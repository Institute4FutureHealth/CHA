import os
from unittest.mock import MagicMock

import pytest
from llms import initialize_llm
from llms import LLM_TO_CLASS
from llms import LLMType


def test_initialize_llm_valid_type():
    llm_type = LLMType.OPENAI
    llm_instance = initialize_llm(llm=llm_type)
    assert isinstance(llm_instance, LLM_TO_CLASS[llm_type])


def test_initialize_llm_invalid_type():
    with pytest.raises(ValueError):
        initialize_llm(llm="unknown_type")


def test_initialize_llm_with_kwargs():
    llm_type = LLMType.OPENAI
    kwargs = {"api_key": os.environ["OPENAI_API_KEY"]}
    llm_instance = initialize_llm(llm=llm_type, **kwargs)
    assert isinstance(llm_instance, LLM_TO_CLASS[llm_type])
    assert llm_instance.api_key == os.environ["OPENAI_API_KEY"]


def test_initialize_llm_with_mock():
    llm_type = "unknown_type"
    mocked_llm_class = MagicMock
    with pytest.raises(ValueError):
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "llms.types.LLM_TO_CLASS",
                {"unknown_type": mocked_llm_class},
            )
            initialize_llm(llm=llm_type)
