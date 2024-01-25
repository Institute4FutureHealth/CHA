"""
Sress Recommendation - Stress estimation
"""
import json
from typing import Any
from typing import List

import neurokit2 as nk
import pandas as pd

from tasks.stress_recom.base import Stress_Recom


class SRStressExtraction(Stress_Recom):
    """
    **Description:**

        This tasks performs stress estimation on the provided HR and HRV parameters.
    """

    name: str = "stress_stress_estimation"
    chat_name: str = "StressStressEstimation"
    description: str = (
        "When a request for stress estimation is received, "
        "call this analysis tool. This tool is specifically designed to perform stress estimation using HR and HRV parameters, "
    )
    dependencies: List[str] = ["stress_recom_hr_hrv_extraction"]
    inputs: List[str] = [
        "You should provide the data source, which is in form of datapipe:datapipe_key "
        "the datapipe_key should be extracted from the result of previous actions.",
    ]
    outputs: List[str] = [
        "returns an array of json objects which contains the following keys:"
        "\n**Stress_Level**: The stress level."
    ]
    # False if the output should directly passed back to the planner.
    # True if it should be stored in datapipe
    output_type: bool = True

    def stress_level_calculator(rmssd: float) -> str:
        if rmssd < 20:
            stress_level = "Very High"
        elif rmssd < 100:
            stress_level = "High"
        elif rmssd < 150:
            stress_level = "Normal"
        elif rmssd < 200:
            stress_level = "Low"
        else:
            stress_level = "Very Low"
        return stress_level

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        hr_hrv = pd.read_json(inputs[0]["data"])
        rmssd = hr_hrv.at[0, 'HRV_RMSSD']
        stress_level = self.stress_level_calculator(rmssd=rmssd)
        df = pd.DataFrame([stress_level], columns=["Stress_Level"])
        json_out = df.to_json(orient="columns")
        return json_out
