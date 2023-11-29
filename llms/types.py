from typing import Dict
from typing import Type

from llms.anthropic import AntropicLLM
from llms.llm import BaseLLM
from llms.llm_types import LLMType
from llms.openai import OpenAILLM

LLM_TO_CLASS: Dict[LLMType, Type[BaseLLM]] = {
    LLMType.OPENAI: OpenAILLM,
    LLMType.ANTHROPIC: AntropicLLM,
}
