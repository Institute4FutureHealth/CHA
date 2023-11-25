from tasks.task import BaseTask
from typing import Any, List, Dict
import json

class ReadDataPipe(BaseTask):
  """
  **Description:** 

    This code reads raw data stored in datapipe. When different tasks are executed, there are situations that the final data is stored 
    in the datapipe when the final called task's output_type=True. In these situations, this task is called to retireve the latest stored data 
    to be used for final inference.
  """

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
    """
        This simply retrieves data from datapipe.

    Args:
        inputs (List[Any]): The datapipe key
    Return:
        str: The raw data along with the instructions.
    
    """
    return "The data along with the description for each data is provided. Use the data and description to provide a detailed answer regarding the user query.\n\n"\
        + json.dumps(inputs[0])

  def explain(
        self,
      ) -> str:
    """
        Provide an explanation of the task.

    Return:
        str: Explanation of the SerpAPI task.

    """
    return (
      "This task is to read data from datapipe."
    )