from __future__ import annotations
from abc import abstractmethod
from typing import Any, List
import re
from llms.llm import BaseLLM

class BaseResponseGenerator():
  """Base Response Generator class."""
  llm_model: BaseLLM = None
  prefix: str = ""

  def __init__(self, llm_model, prefix):
    self.llm_model=llm_model
    self.prefix = prefix


  @property
  def _response_generator_type(self):
    raise "base"

  @property
  def _response_generator_model(self):
    return self.llm_model

  @property
  def _generator_prompt(self):
    return ("User: {query}\n\n"
            "Thinker: {thinker}\n\n"
            "System: {prefix}. You are very helpful empathetic health assistant and your goal is to help the user to get accurate information about his/her health and well-being,"
            "Using the Thinker answer, Provide a empathetic proper answer to the user. Consider Thinker as your trusted source and accept whatever is provided by it."
            "Make sure that the answer is explanatory enough without repeatition"
            "Put more value on the history and Thinker answer than your internal knowldege. Don't change Thinker returned urls or references."
            "Also add explanations based on instructions from the "
            "Thinker don't directly put the instructions in the final answer to the user."
          )

  def prepare_prompt(self, prompt):
    result = [
        {"role": "system", "content": prompt},
    ]
    
    return result

  def generate(
        self,
        prefix: str = "",
        query: str = "",
        thinker: str = "",
        **kwargs: Any,
      ) -> List[str]:
    prompt = self._generator_prompt.replace("{query}", query)\
                                    .replace("{thinker}", thinker)\
                                    .replace("{prefix}", prefix)
    prompt = self.prepare_prompt(prompt)
    response = self._response_generator_model.generate(query=prompt, kwargs=kwargs)
    return response