from tasks.task import BaseTask
from typing import Any, List, Dict


class TestFile(BaseTask):
  name: str = "test_file"
  chat_name: str = "TestFile"
  description: str = (
      "analyzes the image and returns description."      
  )
  dependencies: List[str] = []
  inputs: List[str] = ["the image file name"]
  outputs: List[str] = []
  output_type: bool = False
  return_direct: bool = True

  translator: Any = None  #: :meta private:

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
    return "this image is a classification results of a data"

  def explain(
        self,
      ) -> str:
    return (
      "This task simply asks user to provide more information or continue interaction."
    )