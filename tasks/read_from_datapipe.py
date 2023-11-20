from tasks.task import BaseTask
from typing import Any, List, Dict


class ReadDataPipe(BaseTask):
  name: str = "read_from_datapipe"
  chat_name: str = "DataPipeReader"
  description: str = (
      "This task is to read raw data from datapipe."
      "This task should have the lowest priority."      
  )
  dependencies: List[str] = []
  inputs: List[str] = ["the datapipe key in the format: $datapipe:key$"]
  outputs: List[str] = []
  output_type: bool = False

  translator: Any = None  #: :meta private:

  def _execute(
    self,
    inputs: List[Any],
  ) -> str:
    """Translate query"""
    return inputs[0]

  def explain(
        self,
      ) -> str:
    return (
      "This task is to read data from datapipe."
    )