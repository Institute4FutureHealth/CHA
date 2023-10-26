from __future__ import annotations
from abc import abstractmethod
from typing import List, Optional

class BaseTask():

  name: str
  chat_name: str
  description: str
  dependencies: List[str] = []
  inputs: List[str] = []
  outputs: List[str] = []
  output_type: bool = False

  @property
  def dependencies(self):
    return self.dependencies

  @property
  def inputs(self):
    return ", ".join([f"{str(i)}-{input}" for i, input in enumerate(self.inputs)])

  @abstractmethod
  def execute(
        self,
        input: str,
      ) -> str:
    """
    """

  def parse_input(
        self,
        input: str,
      ) -> List[str]:
    return input.split(",")

  def dict(self):
    prompt = f"{self.name}: {self.description}."
    if len(self.inputs) > 0:
      prompt += f"The input to this tool should be comma separated list of data representing: {self.inputs}"
    if len(self.dependencies) > 0:
      prompt += f"\nThis task is dependent on the following tasks. You need too call these tasks first: {str(self.dependencies)}"
    prompt += "\n"
    return prompt

  def explain(
        self,
      ) -> str:
    return """
      Sample Explanation
    """
