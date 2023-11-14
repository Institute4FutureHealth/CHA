Types
=====




LLM Types
---------


This code defines an Enum called "LLMType" that includes two members: "OPENAI" and "ANTHROPIC".


.. code:: python

    from enum import Enum 

    class LLMType(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"



Types
-----


This code defines a dictionary called "LLM_TO_CLASS" that maps the LLM type to its corresponding class.


.. code:: python

    from typing import Dict, Type, Union

    from llms.llm_types import LLMType
    from llms.llm import BaseLLM
    from llms.openai import OpenAILLM
    from llms.anthropic import AntropicLLM

    LLM_TO_CLASS: Dict[LLMType, Type[BaseLLM]] = {
    LLMType.OPENAI: OpenAILLM,
    LLMType.ANTHROPIC: AntropicLLM
    }


