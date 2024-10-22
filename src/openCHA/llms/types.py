from typing import Dict
from typing import Type

from openCHA.llms import AntropicLLM
from openCHA.llms import BaseLLM
from openCHA.llms import LLMType
from openCHA.llms import OpenAILLM

LLM_TO_CLASS: Dict[LLMType, Type[BaseLLM]] = {
    LLMType.OPENAI: OpenAILLM,
    LLMType.ANTHROPIC: AntropicLLM,
}
