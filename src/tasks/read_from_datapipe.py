import json
from typing import Any
from typing import List

from tasks.task import BaseTask


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
        "Returns the requested datapipe key data. This tool can be called after other tools are executed."
        "This tool should have the lowest priority calling."
        "You should always try to priorities passing the datapipe key to other tool rather than calling this tool."
    )
    dependencies: List[str] = []
    inputs: List[str] = [
        "the datapipe key in the format datapipe:datapipe_key"
    ]
    outputs: List[str] = []
    output_type: bool = False

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        """
            This simply retrieves data from datapipe.

        Args:
            inputs (List[Any]): The datapipe key
        Return:
            str: The raw data along with the instructions.

        """
        if len(inputs) == 0:
            return ""
        return (
            "The data along with the description for each data is provided. "
            "Use the data and description to provide a detailed answer regarding the user query.\n\n"
            + json.dumps(inputs[0])
        )

    def explain(
        self,
    ) -> str:
        """
            Provide an explanation of the task.

        Return:
            str: Explanation of the SerpAPI task.

        """
        return "This task is to read data from datapipe."
