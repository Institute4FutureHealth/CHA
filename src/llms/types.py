from typing import Dict
from typing import Type

from anthropic import AntropicLLM
from llm import BaseLLM
from llm_types import LLMType
from openai import OpenAILLM

LLM_TO_CLASS: Dict[LLMType, Type[BaseLLM]] = {
    LLMType.OPENAI: OpenAILLM,
    LLMType.ANTHROPIC: AntropicLLM,
}
