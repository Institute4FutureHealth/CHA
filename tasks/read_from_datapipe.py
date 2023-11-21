from tasks.task import BaseTask
from typing import Any, List, Dict
import json

class ReadDataPipe(BaseTask):
  name: str = "read_from_datapipe"
  chat_name: str = "DataPipeReader"
  description: str = (
      "Get the stored information from datapipe to be used to answer user query accurately. This should be called when the final answer is in datapipe."
  )
  dependencies: List[str] = []
  inputs: List[str] = ["the datapipe key in the format $datapipe:key$"]
  outputs: List[str] = []
  output_type: bool = False

  def _execute(
    self,
    inputs: List[Any],
  ) -> str:
    """Translate query"""
    return "The data along with the description for each data is provided. Use the data and description to provide a detailed answer regarding the user query.\n\n"\
        + json.dumps(inputs[0])

  def explain(
        self,
      ) -> str:
    return (
      "This task is to read data from datapipe."
    )