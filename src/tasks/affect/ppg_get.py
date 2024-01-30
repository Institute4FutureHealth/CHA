import os
from typing import Any
from typing import List

from tasks.affect.base import Affect


class PPGGet(Affect):
    """
    **Description:**

        This tasks gets ppg affect data for specific patient.
    """

    name: str = "affect_ppg_get"
    chat_name: str = "AffectPPGGet"
    description: str = (
        "Returns the ppg data for a specific patient over a date or a period (if two dates are provided). "
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
        "\n**ppg**: is the ppg value."
        "\n**hr (in beats per minute)**: is the heart rate of the patient."
    ]
    # False if the output should directly passed back to the planner.
    # True if it should be stored in datapipe
    output_type: bool = True
    #
    file_name: str = "ppg.csv"
    device_name: str = "samsung"
    local_dir: str = "data/affect"
    columns_to_keep: List[str] = [
        "timestamp",
        "ppg",
        "hr",
    ]
    columns_revised: List[str] = [
        "date",
        "ppg",
        "hr",
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
            date_column="timestamp",
        )
        df.columns = self.columns_revised
        start_indices = df.index[
            (df["hr"] == 0) & (df["hr"].shift(1) != 0)
        ].tolist()
        df = df.loc[start_indices[-2] : start_indices[-1]]
        df = df.round(2)
        json_out = df.to_json(orient="records")
        return json_out
