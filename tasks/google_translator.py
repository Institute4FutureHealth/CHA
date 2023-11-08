"""
A part of the task implementation is borrowed from LangChain: 
https://github.com/langchain-ai/langchain
"""
from tasks.task import BaseTask
from typing import Any, List, Dict
from pydantic import model_validator


class GoogleTranslate(BaseTask):
  name: str = "google_translator"
  chat_name: str = "GoogleTranslator"
  description: str = (
      "Translates queries between different languages."      
  )
  dependencies: List[str] = []
  inputs: List[str] = ["text to be translated", "destination language"]
  outputs: List[str] = []
  output_type: bool = False

  translator: Any = None  #: :meta private:

  @model_validator(mode='before')
  def validate_environment(cls, values: Dict) -> Dict:
    """Validate that api key and python package exists in environment."""    
    try:
      from vtrans import Translator

      values["translator"] = Translator()
    except ImportError:
      raise ValueError(
        "Could not import googletrans python package. "
        "Please install it with `pip install googletrans==4.0.0-rc1`."
      )
    return values

  def parse_input(
        self,
        input: str,
      ) -> List[str]:
    return input.split("$#")

  def execute(
    self,
    input: str,
  ) -> str:
    """Translate query"""
    inputs = self.parse_input(input)
    dest = inputs[1] if inputs[1] is not None else "en" 
    result = self.translator.translate(input[0], dest=dest)
    return result.text, result.src

  def explain(
        self,
      ) -> str:
    return (
      "This task uses google translate to translate between languages"
    )