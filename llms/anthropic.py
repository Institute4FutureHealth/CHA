from __future__ import annotations
from utils import get_from_dict_or_env
from llms.llm import BaseLLM
from typing import Any, List, Dict
from pydantic import model_validator

class AntropicLLM(BaseLLM):
  models: Dict = {
    "claude-2": 100000,    
  }
  llm_model: Any = None
  api_key: str = ""
  HUMAN_PROMPT: str = ""
  AI_PROMPT: str = ""

  @model_validator(mode='before')
  def validate_environment(cls, values: Dict) -> Dict:
    """Validate that api key and python package exists in environment."""
    anthropic_api_key = get_from_dict_or_env(
      values, "anthropic_api_key", "ANTHROPIC_API_KEY"
    )
    values["api_key"] = anthropic_api_key
    try:
      from anthropic import AsyncAnthropic, HUMAN_PROMPT, AI_PROMPT

      values["llm_model"] = AsyncAnthropic
      values["HUMAN_PROMPT"] = HUMAN_PROMPT
      values["AI_PROMPT"] = AI_PROMPT
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
    token_count = self.llm_model(api_key=self.api_key).count_tokens(query)
    return model_max_token < token_count
  
  def parse_response(self, response) -> str:
    return response.completion

  def prepare_prompt(self, prompt) -> Any:    
    return f"{self.HUMAN_PROMPT} {prompt}{self.AI_PROMPT}"

  def generate(
        self,
        query: str,
        **kwargs: Any
      ) -> str: 
        
    model_name = "claude-2"
    if "model_name" in kwargs:
      model_name = kwargs["model_name"]
    if model_name not in self.get_model_names():
      raise ValueError(
        "model_name is not specified or OpenAI does not support provided model_name"
      )

    max_token = kwargs["max_token"] if "max_token" in kwargs else 32000
    query = self.prepare_prompt(query)
    response = self.llm_model(api_key=self.api_key).completions.create(
                                                                        model=model_name,
                                                                        max_tokens_to_sample=max_token,
                                                                        prompt=query,
                                                                      )
    return self.parse_response(response)