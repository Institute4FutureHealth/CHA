from __future__ import annotations
from abc import abstractmethod
from typing import List, Optional
from pydantic import BaseModel

class BaseTask(BaseModel):

  name: str
  chat_name: str
  description: str
  dependencies: List[str] = []
  inputs: List[str] = []
  outputs: List[str] = []
  #False if the output should directly passed back to the planner.
  #True if it should be stored in datapipe
  output_type: bool = False
  #False if planner should continue. True if after this task the planning should be
  #on pause or stop. examples are when you have a task that asks user to provide more information
  return_direct: bool = False

  class Config:
    """Configuration for this pydantic object."""
    arbitrary_types_allowed = True

  def __init__(self, **kwargs):
    super().__init__()

  @property
  def name(self):
    return self.name

  @property
  def dependencies(self):
    return self.dependencies

  @property
  def inputs(self):
    return ", ".join([f"{str(i)}-{input}" for i, input in enumerate(self.inputs)])

  @property
  def output_type(self):
    return self.output_type
  
  @property
  def return_direct(self):
    return self.return_direct

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

  def get_dict(self) -> str:
    inputs = ",".join(self.inputs)
    dependencies = ",".join(self.dependencies)
    prompt = f"tool name:{self.name}, description: {self.description}."
    if len(self.inputs) > 0:
      prompt += f"The input to this tool should be comma separated list of data representing: {inputs}"
    if len(self.dependencies) > 0:
      prompt += f"\nThis tool is dependent on the following tools. make sure these tools are called first: '{dependencies}'"
    # prompt += "\n"
    return prompt

  def explain(
        self,
      ) -> str:
    return """
      Sample Explanation
    """
