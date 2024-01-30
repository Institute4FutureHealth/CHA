import os
from typing import Any
from typing import List

from tasks.affect.base import Affect


class SleepGet(Affect):
    """
    **Description:**

        This tasks gets sleep affect data for specific patient.
    """

    name: str = "affect_sleep_get"
    chat_name: str = "AffectSleepGet"
    description: str = (
        "Returns the sleep data for a specific patient over a date or a period (if two dates are provided). "
        "This will return the detailed raw data and stores it in the datapipe."
    )
    dependencies: List[str] = []
    inputs: List[str] = [
        "user ID in string. It can be refered as user, patient, individual, etc. Start with 'par_' following with a number (e.g., 'par_1').",
        "start date of the sleep data in string with the following format: `%Y-%m-%d`",
        (
            "end date of the sleep data in string with the following format: `%Y-%m-%d`. "
            "If there is no end date, the value should be an empty string (i.e., '')"
        ),
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
    #
    file_name: str = "sleep.csv"
    device_name: str = "oura"
    local_dir: str = "data/affect"
    columns_to_keep: List[str] = [
        "date",
        "total",
        "awake",
        "light",
        "rem",
        "deep",
        "onset_latency",
        "midpoint_time",
        "efficiency",
        "hr_average",
        "hr_lowest",
        "rmssd",
        "breath_average",
        "temperature_delta",
    ]
    columns_revised: List[str] = [
        "date",
        "total_sleep_time",
        "awake_duration",
        "light_sleep_duration",
        "rem_sleep_duration",
        "deep_sleep_duration",
        "sleep_onset_latency",
        "midpoint_time_of_sleep",
        "sleep_efficiency",
        "average_heart_rate",
        "minimum_heart_rate",
        "rmssd",
        "average_breathing_rate",
        "temperature_variation",
    ]
    variables_in_seconds: List[str] = [
        "total_sleep_time",
        "awake_duration",
        "light_sleep_duration",
        "rem_sleep_duration",
        "deep_sleep_duration",
        "sleep_onset_latency",
        "midpoint_time_of_sleep",
    ]

    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        user_id = inputs[0].strip()
        full_dir = os.path.join(
            self.local_dir, user_id, self.device_name
        )
        df = self._get_data(
            local_dir=full_dir,
            file_name=self.file_name,
            start_date=inputs[1].strip(),
            end_date=inputs[2].strip(),
            usecols=self.columns_to_keep,
        )
        df.columns = self.columns_revised
        df = self._convert_seconds_to_minutes(
            df, self.variables_in_seconds
        )
        df = df.round(2)
        json_out = df.to_json(orient="records")
        return json_out
