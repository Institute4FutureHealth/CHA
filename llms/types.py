from typing import Dict, Type, Union

from llms.llm_types import LLMType
from llms.llm import BaseLLM
from llms.openai import OpenAILLM


LLM_TO_CLASS: Dict[LLMType, Type[BaseLLM]] = {
  LLMType.OPENAI: OpenAILLM
}
