import json
from io import StringIO
from typing import Any
from typing import List

import pandas as pd

from tasks.affect.base import Affect


class SleepAnalysis(Affect):
    """
    **Description:**

        This tasks performs average, sum, or trend analysis on the provided raw sleep affect data for specific patient.
    """

    name: str = "affect_sleep_analysis"
    chat_name: str = "AffectSleepAnalysis"
    description: str = (
        "When a request for analysis of sleep data is received (such as calculating averages, sums, or identifying trends), "
        "call this analysis tool. This tool is specifically designed to handle complex data computations on sleep data records, "
        "ensuring precise and reliable results. Example: If the data spans a year and the user seeks an average sleep data, "
        "this tool will calculate the yearly average. If monthly data is needed, this task should be called multiple times for each month."
    )
    dependencies: List[str] = ["affect_sleep_get"]
    inputs: List[str] = [
        "You should provide the data source, which is in form of datapipe:datapipe_key "
        "the datapipe_key should be extracted from the result of previous actions.",
        "the analysis type which is one of **average** or **trend**.",
    ]
    outputs: List[str] = [
        "returns an array of json objects which contains the following keys:"
        "\n**date (in milliseconds)**: epoch format"
        "\n**total_sleep_time (in minutes)**: is Total amount of sleep (a.k.a. sleep duration) registered during the sleep period."
        "\n**awake_duration (in minutes)**: is the total amount of awake time registered during the sleep period."
        "\n**light_sleep_duration (in minutes)**: is the total amount of light (N1 or N2) sleep registered during the sleep period."
        "\n**rem_sleep_duration (in minutes)**: is the total amount of REM sleep registered during the sleep period."
        "\n**deep_sleep_duration (in minutes)**: is the total amount of deep (N3) sleep registered during the sleep period."
        "\n**sleep_onset_latency (in minutes)**: is detected latency from bedtime_start to the beginning of the first"
        "five minutes of persistent sleep."
        "\n**midpoint_time_of_sleep (in minutes)**: is the time from the start of sleep to the midpoint of sleep. The midpoint ignores awake periods."
        "\n**sleep_efficiency**: is the percentage of the sleep period spent asleep (100% * sleep duration / time in bed)."
        "\n**average_heart_rate**: is the average heart rate registered during the sleep period."
        "\n**minimum_heart_rate**: is the lowest heart rate (5 minutes sliding average) registered during the sleep period."
        "\n**rmssd is the average**: Root Mean Square of Successive Differences (RMSSD) registered during the sleep period."
        "\n**average_breathing_rate**: is the average breathing rate registered during the sleep period."
        "\n**temperature_variation**: is the skin temperature deviation from the long-term temperature average."
    ]
    # False if the output should directly passed back to the planner.
    # True if it should be stored in datapipe
    output_type: bool = True

    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        try:
            df = pd.read_json(
                StringIO(inputs[0]["data"].strip()), orient="records"
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return json.loads(
                '{"Data": "No data for the selected date(s)!"}'
            )
        if df.empty:
            return json.loads(
                '{"Data": "No data for the selected date(s)!"}'
            )
        analysis_type = inputs[1].strip()
        if analysis_type == "average":
            df = df.drop("date", axis=1)  # No average for date!
            df = df.mean().to_frame().T
        elif analysis_type == "trend":
            df = self._calculate_slope(df)
        else:
            raise ValueError(
                "The input analysis type has not been defined!"
            )
        df = df.round(2)
        json_out = df.to_json(orient="records")
        return json_out
