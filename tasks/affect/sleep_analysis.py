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
        "Performs trend or average analysis on the provided sleep data. You must Call this whenever sleep trend or average is needed."
        "For example, if the user asks for trends (or variations) in data, you must call this task"
    )
    dependencies: List[str] = ["affect_sleep_get"]
    inputs: List[str] = [
        "datapipe key to the data",
        "analysis_type. It can be one of [average, trend].",
    ]
    outputs: List[str] = [
        (
            "The analysis result for total_sleep_time. Look for analysis_type to find the type of analysis. "
            "total_sleep_time (in minutes) is Total amount of sleep (a.k.a. sleep duration) registered during the sleep period."
        ),
        (
            "The analysis result for awake_duration. Look for analysis_type to find the type of analysis. "
            "awake_duration (in minutes) is the total amount of awake time registered during the sleep period."
        ),
        (
            "The analysis result for light_sleep_duration. Look for analysis_type to find the type of analysis. "
            "light_sleep_duration (in minutes) is the total amount of light (N1 or N2) sleep registered during the sleep period."
        ),
        (
            "The analysis result for rem_sleep_duration. Look for analysis_type to find the type of analysis. "
            "rem_sleep_duration (in minutes) is the total amount of REM sleep registered during the sleep period."
        ),
        (
            "The analysis result for deep_sleep_duration. Look for analysis_type to find the type of analysis. "
            "deep_sleep_duration (in minutes) is the total amount of deep (N3) sleep registered during the sleep period."
        ),
        (
            "The analysis result for sleep_onset_latency. Look for analysis_type to find the type of analysis. sleep_onset_latency (in minutes) "
            "is the detected latency from bedtime_start to the beginning of the first five minutes of persistent sleep."
        ),
        (
            "The analysis result for midpoint_time_of_sleep. Look for analysis_type to find the type of analysis. "
            "midpoint_time_of_sleep (in minutes) is the time from the start of sleep to the midpoint of sleep. The midpoint ignores awake periods."
        ),
        (
            "The analysis result for sleep_efficiency. Look for analysis_type to find the type of analysis. "
            "sleep_efficiency is the percentage of the sleep period spent asleep (100% * sleep duration / time in bed)."
        ),
        (
            "The analysis result for average_heart_rate. Look for analysis_type to find the type of analysis. "
            "average_heart_rate is the average heart rate registered during the sleep period."
        ),
        (
            "The analysis result for minimum_heart_rate. Look for analysis_type to find the type of analysis. "
            "minimum_heart_rate is the lowest heart rate (5 minutes sliding average) registered during the sleep period."
        ),
        (
            "The analysis result for rmssd. Look for analysis_type to find the type of analysis. "
            "rmssd is the average Root Mean Square of Successive Differences (RMSSD) registered during the sleep period."
        ),
        (
            "The analysis result for average_breathing_rate. Look for analysis_type to find the type of analysis. "
            "average_breathing_rate is the average breathing rate registered during the sleep period."
        ),
        (
            "The analysis result for temperature_variation. Look for analysis_type to find the type of analysis. "
            "temperature_variation is the skin temperature deviation from the long-term temperature average."
        ),
    ]
    # False if the output should directly passed back to the planner.
    # True if it should be stored in datapipe
    output_type: bool = True

    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        df = pd.read_json(
            StringIO(inputs[0]["data"].strip()), orient="records"
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
