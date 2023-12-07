import os
from typing import Any
from typing import List

from tasks.affect.base import Affect


class PpgGet(Affect):
    name: str = "affect_ppg_get"
    chat_name: str = "AffectPpgGet"
    description: str = (
        "Get the Photoplethysmogram (PPG) signal for a specific date or "
        "a period of time (if two dates or time points are provided). "
    )
    dependencies: List[str] = []
    inputs: List[str] = [
        "user ID in string. It can be refered as user, patient, individual, etc. Start with 'par_' following with a number (e.g., 'par_1').",
        "start time of the PPG signal in string with the following format: '%Y-%m-%d %H:%M:%S'",
        (
            "end time of the PPG signal in string with the following format: '%Y-%m-%d %H:%M:%S'."
            " If there is no end date, the value should be an empty string (i.e., '')"
        ),
    ]
    outputs: List[str] = [
        (
            "Photoplethysmogram (PPG) is a biomedical signal collected via an optical technique that "
            "indicates synchronous blood volumetric changes in the microvascular bed of tissues."
            " Variations in PPG signals are associated with the oscillation of heartbeat and respiration."
        ),
        "Sampling frequency of the PPG signal",
    ]
    # False if the output should directly passed back to the planner.
    # True if it should be stored in datapipe
    output_type: bool = True
    #
    file_name: str = "ppg.csv"
    device_name: str = "samsung"
    local_dir: str = "data/affect"
    columns_to_keep: List[str] = ["timestamp", "ppg"]

    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        user_id = inputs[0].strip()
        full_dir = os.path.join(
            self.local_dir, user_id, self.device_name
        )
        # Import the data as dataframe
        df = self._get_data_with_timestamp(
            local_dir=full_dir,
            file_name=self.file_name,
            start_date=inputs[1].strip(),
            end_date=inputs[2].strip(),
        )
        if df.empty:
            self.output_type = False
            return "No data is available for the selected period."
        df = df[self.columns_to_keep]

        # Sampling frequency of the signals is 20 Hz
        sampling_frequency = 20

        # Convert the whole dataframe into a list of 5 minute data chuncks
        df_ppg_chunks = self._split_dataframe_by_time(
            df=df,
            sampling_frequency=sampling_frequency,
            window_length=5,
        )

        # Convert the output to json
        json_out = self._ppg_dataframes_and_fs_to_json(
            dataframes_list=df_ppg_chunks,
            sampling_frequency=sampling_frequency,
        )
        return json_out
