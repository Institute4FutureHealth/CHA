from __future__ import annotations
from abc import abstractmethod
from typing import List, Any
from datapipes.datapipe import DataPipe
from pydantic import BaseModel
import json
import re

class BaseTask(BaseModel):

  name: str
  chat_name: str
  description: str
  dependencies: List[str] = []
  inputs: List[str] = []
  outputs: List[str] = []
  datapipe: DataPipe = None
  #False if the output should directly passed back to the planner.
  #True if it should be stored in datapipe
  output_type: bool = False
  #False if planner should continue. True if after this task the planning should be
  #on pause or stop. examples are when you have a task that asks user to provide more information
  return_direct: bool = False

  class Config:
    """Configuration for this pydantic object."""
    arbitrary_types_allowed = True

  @property
  def name(self):
    return self.name

  @property
  def dependencies(self):
    return self.dependencies

  @property
  def inputs(self):
    return ", ".join([f"{str(i)}-{input}" for i, input in enumerate(self.inputs)])

  @abstractmethod
  def _execute(
        self,
        inputs: List[Any],
      ) -> str:
    """
    """

  def _parse_input(
        self,
        input_args: str,
      ) -> List[str]:
    inputs = input_args.split(",")
    return [json.loads(self.datapipe.retrieve(re.search(r"datapipe:[0-9a-f\-]{36}", arg).group().strip().split(":")[-1])) if "datapipe" in arg else arg.strip() for arg in inputs]

  def _post_execute(
          self,
          result
        ):
    if self.output_type:
      key = self.datapipe.store(json.dumps({'data': result, 'description': ",".join(self.outputs)}))      
      return (
        f"The result of the tool {self.name} is stored in the datapipe with key: $datapipe:{key}$"
        " pass this key to other tools to access to the result or call read_from_datapipe to get the raw data."
      )
    return result

  def execute(
        self,
        input_args: str
      ) -> str:
    inputs = self._parse_input(input_args)
    result = self._execute(inputs)
    return self._post_execute(result)

  def get_dict(self) -> str:
    inputs = ",".join(f"input{i+1}-{word}" for i, word in enumerate(self.inputs))
    dependencies = ",".join(f"{i+1}-{word}" for i, word in enumerate(self.dependencies))
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
