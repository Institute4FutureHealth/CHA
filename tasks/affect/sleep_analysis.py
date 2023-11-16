'''
Affect - Sleep Analysis
'''

from typing import List, Any
import os
from tasks.affect.base import Affect


class SleepAnalysis(Affect):
    name: str = "affect_sleep_analysis"
    chat_name: str = "AffectSleepAnalysis"
    description: str = ("Analyze the sleep data. You must Call this whenever sleep analysis (e.g., 'average' or 'trend') is needed. DON'T rely on your analysis."
                        "For example, if the user asks for trends (or variations) in data, you must call this task")
    dependencies: List[str] = ["affect_sleep_get"]
    inputs: List[str] = ["It is an string but in Pandas dataframe format. It is the output of the $affect_sleep_get$",
                         "analysis_type. It can be one of [$average$, $trend$]."]
    outputs: List[str] = ["The analysis result for total_sleep_time. Look for analysis_type to find the type of analysis. total_sleep_time (in minutes) is Total amount of sleep (a.k.a. sleep duration) registered during the sleep period.",
                          "The analysis result for awake_duration. Look for analysis_type to find the type of analysis. awake_duration (in minutes) is the total amount of awake time registered during the sleep period.",
                          "The analysis result for light_sleep_duration. Look for analysis_type to find the type of analysis. light_sleep_duration (in minutes) is the total amount of light (N1 or N2) sleep registered during the sleep period.",
                          "The analysis result for rem_sleep_duration. Look for analysis_type to find the type of analysis. rem_sleep_duration (in minutes) is the total amount of REM sleep registered during the sleep period.",
                          "The analysis result for deep_sleep_duration. Look for analysis_type to find the type of analysis. deep_sleep_duration (in minutes) is the total amount of deep (N3) sleep registered during the sleep period.",
                          "The analysis result for sleep_onset_latency. Look for analysis_type to find the type of analysis. sleep_onset_latency (in minutes) is the detected latency from bedtime_start to the beginning of the first five minutes of persistent sleep.",
                          "The analysis result for midpoint_time_of_sleep. Look for analysis_type to find the type of analysis. midpoint_time_of_sleep (in minutes) is the time from the start of sleep to the midpoint of sleep. The midpoint ignores awake periods.",
                          "The analysis result for sleep_efficiency. Look for analysis_type to find the type of analysis. sleep_efficiency is the percentage of the sleep period spent asleep (100% * sleep duration / time in bed).",
                          "The analysis result for average_heart_rate. Look for analysis_type to find the type of analysis. average_heart_rate is the average heart rate registered during the sleep period.",
                          "The analysis result for minimum_heart_rate. Look for analysis_type to find the type of analysis. minimum_heart_rate is the lowest heart rate (5 minutes sliding average) registered during the sleep period.",
                          "The analysis result for rmssd. Look for analysis_type to find the type of analysis. rmssd is the average Root Mean Square of Successive Differences (RMSSD) registered during the sleep period.",
                          "The analysis result for average_breathing_rate. Look for analysis_type to find the type of analysis. average_breathing_rate is the average breathing rate registered during the sleep period.",
                          "The analysis result for temperature_variation. Look for analysis_type to find the type of analysis. temperature_variation is the skin temperature deviation from the long-term temperature average."]
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


    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        #checking
        print("task inside ", inputs)
        df = self._string_output_to_dataframe(inputs[0].strip())
        analysis_type = inputs[1].strip()
        if analysis_type == 'average':
            # df = df.drop('date', axis=1)  # No average for date!
            df_out = df.mean().to_frame().T
        elif analysis_type == 'trend':
            df_out = self._calculate_slope(df)
        else:
            raise ValueError('The input analysis type has not been defined!')
        df_out = df_out.round(2)
        return self._dataframe_to_string_output(df_out)
