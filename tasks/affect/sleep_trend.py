'''
Affect - Sleep Average
'''

from typing import List
from tasks.affect.base import Affect


class SleepTrend(Affect):
    name: str = "sleep_trend"
    chat_name: str = "SleepTrend"
    description: str = "Return the sleep trend (i.e., variation or slope) between start date and end date"
    dependencies: List[str] = []
    inputs: List[str] = ["start date of the sleep data in string with the following format: '%Y-%m-%d'",
                         "end date of the sleep data in string with the following format: '%Y-%m-%d'"]
    outputs: List[str] = ["Trend of total_sleep_time (slope of the fitted line). total_sleep_time (in minutes) is Total amount of sleep (a.k.a. sleep duration) registered during the sleep period.",
                          "Trend of awake_duration (slope of the fitted line). awake_duration (in minutes) is the total amount of awake time registered during the sleep period.",
                          "Trend of light_sleep_duration (slope of the fitted line). light_sleep_duration (in minutes) is the total amount of light (N1 or N2) sleep registered during the sleep period.",
                          "Trend of rem_sleep_duration (slope of the fitted line). rem_sleep_duration (in minutes) is the total amount of REM sleep registered during the sleep period.",
                          "Trend of deep_sleep_duration (slope of the fitted line). deep_sleep_duration (in minutes) is the total amount of deep (N3) sleep registered during the sleep period.",
                          "Trend of sleep_onset_latency (slope of the fitted line). sleep_onset_latency (in minutes) is the detected latency from bedtime_start to the beginning of the first five minutes of persistent sleep.",
                          "Trend of midpoint_time_of_sleep (slope of the fitted line). midpoint_time_of_sleep (in minutes) is the time from the start of sleep to the midpoint of sleep. The midpoint ignores awake periods.",
                          "Trend of sleep_efficiency (slope of the fitted line). sleep_efficiency is the percentage of the sleep period spent asleep (100% * sleep duration / time in bed).",
                          "Trend of average_heart_rate (slope of the fitted line). average_heart_rate is the average heart rate registered during the sleep period.",
                          "Trend of minimum_heart_rate (slope of the fitted line). minimum_heart_rate is the lowest heart rate (5 minutes sliding average) registered during the sleep period.",
                          "Trend of rmssd (slope of the fitted line). rmssd is the average Root Mean Square of Successive Differences (RMSSD) registered during the sleep period.",
                          "Trend of average_breathing_rate (slope of the fitted line). average_breathing_rate is the average breathing rate registered during the sleep period.",
                          "Trend of temperature_variation (slope of the fitted line). temperature_variation is the skin temperature deviation from the long-term temperature average."]
    #False if the output should directly passed back to the planner.
    #True if it should be stored in datapipe
    output_type: bool = False
    #
    file_name: str = 'sleep.csv'
    local_dir: str = 'data/affect'
    columns_to_keep: List[str] = ['date', 'total', 'awake', 'light', 'rem', 'deep',
                                  'onset_latency', 'midpoint_time',
                                  'efficiency', 'hr_average',
                                  'hr_lowest', 'rmssd', 'breath_average',
                                  'temperature_delta']
    columns_revised: List[str] = ['date', 'total_sleep_time', 'awake_duration', 'light_sleep_duration',
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
        df = self._get_data(
            local_dir=self.local_dir,
            file_name=self.file_name,
            start_date=inputs[0].strip(),
            end_date=inputs[1].strip(),
            )
        df = df.loc[:, self.columns_to_keep]
        df.columns = self.columns_revised
        df_out = self._calculate_slope(df)
        df_out = self._convert_seconds_to_minutes(df_out, self.variables_in_seconds)
        df_out = df_out.round(2)
        return self._dataframe_to_string_output(df_out)
