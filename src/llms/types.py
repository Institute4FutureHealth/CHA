from typing import Dict
from typing import Type

from llms import AntropicLLM
from llms import BaseLLM
from llms import LLMType
from llms import OpenAILLM

LLM_TO_CLASS: Dict[LLMType, Type[BaseLLM]] = {
    LLMType.OPENAI: OpenAILLM,
    LLMType.ANTHROPIC: AntropicLLM,
}
