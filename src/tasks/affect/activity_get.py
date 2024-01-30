"""
Affect - Get physical activity data
"""
import os
from typing import Any
from typing import List

from tasks.affect.base import Affect


class ActivityGet(Affect):
    """
    **Description:**

        This tasks gets activity affect data for specific patient.
    """

    name: str = "affect_activity_get"
    chat_name: str = "AffectActivityGet"
    description: str = "Gathers physical activity data for a patient over a certain period."
    dependencies: List[str] = []
    inputs: List[str] = [
        (
            "user ID in string. It can be refered as user, patient, individual, etc. The input format should be: "
            "par_<user_id> for example for user 1 it will be par_1."
        ),
        "start date of the physical activity data with the following format: '%Y-%m-%d'",
        "end date of the physical activity data with the following format: '%Y-%m-%d'.",
    ]
    outputs: List[str] = [
        "returns an array of json objects which contains the following keys:"
        "\n**steps_count**: is the total number of steps registered during the day."
        "\n**rest_time**: is the time (in minutes) during the day spent resting, i.e. sleeping or lying down.",
        "\n**inactive_time**: is the time (in minutes) during the day spent resting, i.e. sitting or standing still.",
        "\n**low_acitivity_time** is the (in minutes) during the day with low intensity activity (e.g. household work).",
        "\n**medimum_acitivity_time** is the (in minutes) during the day with medium intensity activity (e.g. walking).",
        "\n**high_acitivity_time** is the (in minutes) during the day with high intensity activity (e.g. running).",
    ]

    # False if the output should directly passed back to the planner.
    # True if it should be stored in datapipe
    output_type: bool = True
    #
    file_name: str = "activity.csv"
    device_name: str = "oura"
    local_dir: str = "data/affect"

    columns_to_keep: List[str] = [
        "date",
        "steps",
        "rest",
        "inactive",
        "low",
        "medium",
        "high",
    ]
    columns_revised: List[str] = [
        "date",
        "steps_count",
        "rest_time",
        "inactive_time",
        "low_acitivity_time",
        "medimum_acitivity_time",
        "high_acitivity_time",
    ]

    def _execute(
        self,
        inputs: List[Any] = None,
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
        df = df.round(2)
        json_out = df.to_json(orient="records")
        return json_out
