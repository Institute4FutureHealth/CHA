'''
Affect - Sleep Average
'''

from typing import List
import os
from tasks.affect.base import Affect


class SleepGet(Affect):
    name: str = "affect_sleep_get"
    chat_name: str = "AffectSleepGet"
    description: str = "Get the sleep parameters for a specific date"
    dependencies: List[str] = []
    inputs: List[str] = ["user ID in string. It can be refered as user, patient, individual, etc. Start with 'par_' following with a number (e.g., 'par_1').",
                         "Date of the sleep data in string with the following format: '%Y-%m-%d'"]
    outputs: List[str] = ["total_sleep_time (in minutes) is Total amount of sleep (a.k.a. sleep duration) registered during the sleep period.",
                          "awake_duration (in minutes) is the total amount of awake time registered during the sleep period.",
                          "light_sleep_duration (in minutes) is the total amount of light (N1 or N2) sleep registered during the sleep period.",
                          "rem_sleep_duration (in minutes) is the total amount of REM sleep registered during the sleep period.",
                          "deep_sleep_duration (in minutes) is the total amount of deep (N3) sleep registered during the sleep period.",
                          "sleep_onset_latency (in minutes) is the detected latency from bedtime_start to the beginning of the first five minutes of persistent sleep.",
                          "midpoint_time_of_sleep (in minutes) is the time from the start of sleep to the midpoint of sleep. The midpoint ignores awake periods.",
                          "sleep_efficiency is the percentage of the sleep period spent asleep (100% * sleep duration / time in bed).",
                          "average_heart_rate is the average heart rate registered during the sleep period.",
                          "minimum_heart_rate is the lowest heart rate (5 minutes sliding average) registered during the sleep period.",
                          "rmssd is the average Root Mean Square of Successive Differences (RMSSD) registered during the sleep period.",
                          "average_breathing_rate is the average breathing rate registered during the sleep period.",
                          "temperature_variation is the skin temperature deviation from the long-term temperature average."]
    #False if the output should directly passed back to the planner.
    #True if it should be stored in datapipe
    output_type: bool = False
    #
    file_name: str = 'sleep.csv'
    device_name: str = 'oura'
    local_dir: str = 'data/affect'
    columns_to_keep: List[str] = ['total', 'awake', 'light', 'rem', 'deep',
                                  'onset_latency', 'midpoint_time',
                                  'efficiency', 'hr_average',
                                  'hr_lowest', 'rmssd', 'breath_average',
                                  'temperature_delta']
    columns_revised: List[str] = ['total_sleep_time', 'awake_duration', 'light_sleep_duration',
                                  'rem_sleep_duration', 'deep_sleep_duration',
                                  'sleep_onset_latency', 'midpoint_time_of_sleep',
                                  'sleep_efficiency', 'average_heart_rate',
                                  'minimum_heart_rate', 'rmssd', 'average_breathing_rate',
                                  'temperature_variation']
    variables_in_seconds: List[str] = ['total_sleep_time', 'awake_duration', 'light_sleep_duration',
                                       'rem_sleep_duration', 'deep_sleep_duration',
                                       'sleep_onset_latency', 'midpoint_time_of_sleep']


    def execute(
        self,
        input: str,
    ) -> str:
        inputs = self.parse_input(input)
        #checking
        user_id = inputs[0].strip()
        full_dir = os.path.join(self.local_dir, user_id, self.device_name)
        df = self._get_data(
            local_dir=full_dir,
            file_name=self.file_name,
            start_date=inputs[1].strip(),
            )
        df = self._convert_seconds_to_minutes(df, self.variables_in_seconds)
        df = df.round(2)
        return self._dataframe_to_string_output(df)
