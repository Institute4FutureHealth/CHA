'''
Affect - Get physical activity data
'''

from typing import List, Any
import os
from tasks.affect.base import Affect


class ActivityGet(Affect):
    name: str = "affect_activity_get"
    chat_name: str = "AffectActivityGet"
    description: str = ("Get the physical activity parameters for a specific date or "
                        "a period (if two dates are provided). "
                        "You must Call $affect_analysis$ whenever physical activity "
                        "analysis (e.g., 'average', 'sum', or 'trend') is needed. DON'T rely on your analysis")
    dependencies: List[str] = []
    inputs: List[str] = ["user ID in string. It can be refered as user, patient, individual, etc. Start with 'par_' following with a number (e.g., 'par_1').",
                         "start date of the physical activity data in string with the following format: '%Y-%m-%d'",
                         "end date of the physical activity data in string with the following format: '%Y-%m-%d'. If there is no end date, the value should be an empty string (i.e., '')"]
    outputs: List[str] = ["steps_count is the total number of steps registered during the day.",
                          "rest_time is the time (in minutes) during the day spent resting, i.e. sleeping or lying down.",
                          "inactive_time is the time (in minutes) during the day spent resting, i.e. sitting or standing still.",
                          "low_acitivity_time is the (in minutes) during the day with low intensity activity (e.g. household work).",
                          "medimum_acitivity_time is the (in minutes) during the day with medium intensity activity (e.g. walking).",
                          "high_acitivity_time is the (in minutes) during the day with high intensity activity (e.g. running)."]

    #False if the output should directly passed back to the planner.
    #True if it should be stored in datapipe
    output_type: bool = True
    #
    file_name: str = 'activity.csv'
    device_name: str = 'oura'
    local_dir: str = 'data/affect'

    columns_to_keep: List[str] = ['date', 'steps', 'rest', 'inactive', 'low', 'medium', 'high']
    columns_revised: List[str] = ['date', 'steps_count', 'rest_time', 'inactive_time', 'low_acitivity_time',
                                  'medimum_acitivity_time', 'high_acitivity_time']


    def execute(
        self,
        inputs: List[Any],
    ) -> str:
        user_id = inputs[0].strip()
        full_dir = os.path.join(self.local_dir, user_id, self.device_name)
        df = self._get_data(
            local_dir=full_dir,
            file_name=self.file_name,
            start_date=inputs[1].strip(),
            end_date=inputs[2].strip(),
            usecols=self.columns_to_keep
            )
        df.columns = self.columns_revised
        df = df.round(2)
        json_out = df.to_json(orient='records')
        return json_out
