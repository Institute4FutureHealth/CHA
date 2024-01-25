"""
Sress Recommendation - Physical activity analysis
"""
import json
from typing import Any
from typing import List

import neurokit2 as nk
import pandas as pd

from tasks.stress_recom.base import Stress_Recom


class SRHRHRVExtraction(Stress_Recom):
    """
    **Description:**

        This tasks performs hrv analysis on the provided raw ppg data.
    """

    name: str = "stress_recom_hr_hrv_extraction"
    chat_name: str = "StressRecomHrHrvExtraction"
    description: str = (
        "When a request for analysis of ppg data is received, "
        "call this analysis tool. This tool is specifically designed to perform hrv analysis on ppg records, "
    )
    dependencies: List[str] = ["stress_ppg_get"]
    inputs: List[str] = [
        "You should provide the data source, which is in form of datapipe:datapipe_key "
        "the datapipe_key should be extracted from the result of previous actions.",
    ]
    outputs: List[str] = [
        "returns an array of json objects which contains the following keys:"
        "\n**HRV_MeanNN**: The mean of the RR intervals."
        "\n**HRV_RMSSD**: The square root of the mean of the squared successive differences between adjacent RR intervals.",
        "\n**Heart_Rate** the mean heart rate after stimulus onset.",
    ]
    # False if the output should directly passed back to the planner.
    # True if it should be stored in datapipe
    output_type: bool = True

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        ppg = json.loads(inputs[0]["data"])
        sampling_rate = 1000
        df = None

        ppg_signals, info = nk.ppg_process(ppg, sampling_rate=sampling_rate)
        df = nk.ppg_analyze(ppg_signals, sampling_rate=sampling_rate)
        if df is None:
            df = nk.ppg_analyze(ppg_signals, sampling_rate=sampling_rate)
        else:
            df = pd.concat(
                [
                    df,
                    nk.ppg_analyze(ppg_signals, sampling_rate=sampling_rate),
                ],
                axis=0,
                ignore_index=True,
            )
        df.dropna(how="all", axis=1, inplace=True)
        df = df[
            [
                "HRV_MeanNN",
                "HRV_RMSSD",
                "PPG_Rate_Mean",
            ]
        ]
        df = df.round(2)
        json_out = df.to_json(orient="columns")
        return json_out
