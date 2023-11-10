'''
Affect - Sleep Average
'''

from tasks.affect.base import Affect
from typing import List


class SleepAVG(Affect):
    name: str = "sleep_avg"
    chat_name: str = "SleepAVG"
    description: str = "Return the sleep average between start date and end date"
    dependencies: List[str] = []
    inputs: List[str] = ["start date of the sleep data in string with the following format: '%Y-%m-%d'",
                         "end date of the sleep data in string with the following format: '%Y-%m-%d'"]
    outputs: List[str] = ["sleep_duration is XXX"]
    #False if the output should directly passed back to the planner.
    #True if it should be stored in datapipe
    output_type: bool = False
    #
    file_name: str = 'sleep.csv'
    local_dir: str = 'data/affect'
    columns_to_keep: List[str] = ['duration', 'awake', 'light', 'rem', 'deep',
                                  'onset_latency', 'midpoint_time',
                                  'efficiency', 'hr_average',
                                  'hr_lowest', 'rmssd', 'breath_average',
                                  'temperature_delta', 'bedtime_start_timestamp',
                                  'bedtime_end_timestamp']
    columns_revised: List[str] = ['sleep_duration', 'awake_duration', 'light_sleep_duration',
                                  'rem_sleep_duration', 'deep_sleep_duration',
                                  'sleep_onset_latency', 'midpoint_time_of_sleep',
                                  'sleep_efficiency', 'average_heart_rate',
                                  'minimum_heart_rate', 'rmssd', 'average_breathing_rate',
                                  'temperature_variation', 'bedtime_start',
                                  'bedtime_end']


    def execute(
        self,
        input: str,
    ) -> str:
        inputs = self.parse_input(input)
        #checking
        df = self._get_data(
            local_dir=self.local_dir,
            file_name=self.file_name,
            start_date=inputs[0].strip(),
            end_date=inputs[1].strip(),
            )
        df = df.loc[:, self.columns_to_keep]
        df.columns = self.columns_revised
        df_avg = df.mean()
        return self._dataframe_to_string_output(df_avg)
