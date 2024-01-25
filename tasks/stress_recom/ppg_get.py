import os
from typing import Any
from typing import List

from tasks.stress_recom.base import Stress_Recom


class SRPPGGet(Stress_Recom):
    """
    **Description:**

        This tasks gets ppg data.
    """

    name: str = "stress_recom_ppg_get"
    chat_name: str = "StressRecomPPGGet"
    description: str = (
        "Returns the most recent ppg data. "
        "This will return the detailed raw data and stores it in the datapipe."
    )
    dependencies: List[str] = []
    inputs: List[str] = []
    outputs: List[str] = [
        "returns an array of json objects which contains the following keys:"
        "\n**ppg**: is the ppg value."
    ]
    # False if the output should directly passed back to the planner.
    # True if it should be stored in datapipe
    output_type: bool = True
    #
    file_name: str = "data.csv"
    local_dir: str = "data/stres_recom"
    columns_to_keep: List[str] = [
        "PPG_Raw",
    ]
    columns_revised: List[str] = [
        "ppg",
    ]

    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        full_dir = os.path.join(
            self.local_dir
        )
        df = self._get_data(
            local_dir=full_dir,
            file_name=self.file_name,
            usecols=self.columns_to_keep,
        )
        df.columns = self.columns_revised
        df = df.round(2)
        json_out = df.to_json(orient="records")
        return json_out
