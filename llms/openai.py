import os
from utils import get_from_dict_or_env
from llms.llm import BaseLLM
from typing import Any, List, Dict
from pydantic import model_validator

class OpenAILLM(BaseLLM):
  models: Dict = {
    "gpt-4": 8192,
    "gpt-4-0314": 8192,
    "gpt-4-0613": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-32k-0314": 32768,
    "gpt-4-32k-0613": 32768,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-0301": 4096,
    "gpt-3.5-turbo-0613": 4096,
    "gpt-3.5-turbo-16k": 16385,
    "gpt-3.5-turbo-16k-0613": 16385,
    "text-ada-001": 2049,
    "ada": 2049,
    "text-babbage-001": 2040,
    "babbage": 2049,
    "text-curie-001": 2049,
    "curie": 2049,
    "davinci": 2049,
    "text-davinci-003": 4097,
    "text-davinci-002": 4097,
    "code-davinci-002": 8001,
    "code-davinci-001": 8001,
    "code-cushman-002": 2048,
    "code-cushman-001": 2048,
  }
  api_key: str = ""
  llm_model: Any = None
  max_tokens: int = 150

  @model_validator(mode='before')
  def validate_environment(cls, values: Dict) -> Dict:
    """Validate that api key and python package exists in environment."""
    openai_api_key = get_from_dict_or_env(
      values, "openai_api_key", "OPENAI_API_KEY"
    )
    values["api_key"] = openai_api_key
    try:
      import openai 

      values["llm_model"] = openai
    except ImportError:
      raise ValueError(
        "Could not import anthropic python package. "
        "Please install it with `pip install anthropic`."
      )
    return values

  def get_model_names(self) -> List[str]:
    return self.models.keys()

  def is_max_token(self, model_name, query) -> bool:
    model_max_token = self.models[model_name]
    try:
      import tiktoken
    except ImportError:
      raise ValueError(
        "Could not import tiktoken python package. "
        "This is needed in order to calculate get_num_tokens. "
        "Please install it with `pip install tiktoken`."
      )
    encoder = "gpt2"
    if self.model_name in ("text-davinci-003", "text-davinci-002"):
      encoder = "p50k_base"
    if self.model_name.startswith("code"):
      encoder = "p50k_base"
    
    enc = tiktoken.get_encoding(encoder)
    tokenized_text = enc.encode(query)
    return model_max_token < len(tokenized_text)
  
  def parse_response(self, response) -> str:
    return response.choices[0].message.content

  def prepare_prompt(self, prompt) -> Any:    
    return [{"role": "system", "content": prompt}]

  def generate(
        self,
        query: str,
        **kwargs: Any
      ) -> str: 
        
    model_name = "gpt-3.5-turbo-16k"
    if "model_name" in kwargs:
      model_name = kwargs["model_name"]
    if model_name not in self.get_model_names():
      raise ValueError(
        "model_name is not specified or OpenAI does not support provided model_name"
      )

    stop = kwargs["stop"] if "stop" in kwargs else None
    max_tokens = kwargs["max_tokens"] if "max_tokens" in kwargs else self.max_tokens

    self.llm_model.api_key = self.api_key
    query = self.prepare_prompt(query)
    response = self.llm_model.ChatCompletion.create(model=model_name, messages=query, max_tokens=max_tokens, stop=stop)
    return self.parse_response(response)