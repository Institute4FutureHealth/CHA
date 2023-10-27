import openai 
import os
from utils import get_from_dict_or_env
from llms.llm import BaseLLM
from typing import Any

class OpenAILLM(BaseLLM):
  models = {
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

  def get_model_names(self):
    return self.models.keys()

  def is_max_token(self, model_name, query):
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

  def convert_query(self, query):
    return [{ "role": "user", "content": query }]
  
  def parse_response(self, response):
    return response.choices[0].message.content

  def generate(
        self,
        query: str,
        **kwargs: Any
      ) -> str: 
    
    api_key = get_from_dict_or_env(kwargs, "openai_api_key", "OPENAI_API_KEY")
    model_name = "gpt-3.5-turbo"
    if "model_name" in kwargs:
      model_name = kwargs["model_name"]
    if model_name not in self.get_model_names():
      raise ValueError(
        "model_name is not specified or OpenAI does not support provided model_name"
      )

    openai.api_key = api_key
    response = openai.ChatCompletion.create(model=model_name, messages=self.convert_query(query))
    return self.parse_response(response)