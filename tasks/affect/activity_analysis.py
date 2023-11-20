'''
Affect - Physical activity analysis
'''

from typing import List, Any
import pandas as pd
from tasks.affect.base import Affect
from io import StringIO


class ActivityAnalysis(Affect):
    name: str = "affect_activity_analysis"
    chat_name: str = "AffectActivityAnalysis"
    description: str = ("Analyze the physical activity data. You must Call this whenever physical activity analysis (e.g., 'average', 'sum', or 'trend') is needed. DON'T rely on your analysis."
                        "For example, if the user asks for trends (or variations) in data, you must call this task")
    dependencies: List[str] = ["affect_activity_get"]
    inputs: List[str] = ["It is an string but in json format. It is the output of the $affect_activity_get$",
                         "analysis_type. It can be one of [$average$, $sum$, $trend$]."]
    outputs: List[str] = ["The analysis result for steps_count. Look for analysis_type to find the type of analysis. steps_count is the total number of steps registered during the day.",
                          "The analysis result for rest_time. Look for analysis_type to find the type of analysis. rest_time is the time (in minutes) during the day spent resting, i.e. sleeping or lying down.",
                          "The analysis result for inactive_time. Look for analysis_type to find the type of analysis. inactive_time is the time (in minutes) during the day spent resting, i.e. sitting or standing still.",
                          "The analysis result for low_acitivity_time. Look for analysis_type to find the type of analysis. low_acitivity_time is the (in minutes) during the day with low intensity activity (e.g. household work).",
                          "The analysis result for medimum_acitivity_time. Look for analysis_type to find the type of analysis. medimum_acitivity_time is the (in minutes) during the day with medium intensity activity (e.g. walking).",
                          "The analysis result for high_acitivity_time. Look for analysis_type to find the type of analysis. high_acitivity_time is the (in minutes) during the day with high intensity activity (e.g. running)."]
    #False if the output should directly passed back to the planner.
    #True if it should be stored in datapipe
    output_type: bool = False


    def execute(
        self,
        inputs: List[Any],
    ) -> str:
        df = pd.read_json(StringIO(inputs[0].strip()), orient='records')
        analysis_type = inputs[1].strip()
        if analysis_type == 'average':
            df = df.drop('date', axis=1)  # No average for date!
            df = df.mean().to_frame().T
        elif analysis_type == 'sum':
            df = df.drop('date', axis=1)  # No sum for date!
            df = df.sum().to_frame().T
        elif analysis_type == 'trend':
            df = self._calculate_slope(df)
        else:
            raise ValueError('The input analysis type has not been defined!')
        df = df.round(2)
        json_out = df.to_json(orient='records')
        return json_out
