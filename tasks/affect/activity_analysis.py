"""
Affect - Physical activity analysis
"""
import json
from io import StringIO
from typing import Any
from typing import List

import pandas as pd

from tasks.affect.base import Affect


class ActivityAnalysis(Affect):
    """
    **Description:**

        This tasks performs average, sum, or trend analysis on the provided raw activity affect data for specific patient.
    """

    name: str = "affect_activity_analysis"
    chat_name: str = "AffectActivityAnalysis"
    description: str = (
        "When a request for analysis of physical activity data is received (such as calculating averages, sums, or identifying trends), "
        "call this analysis tool. This tool is specifically designed to handle complex data computations on physical activity records, "
        "ensuring precise and reliable results. Example: If the data spans a year and the user seeks an average activity level, "
        "this tool will calculate the yearly average."
    )
    dependencies: List[str] = ["affect_activity_get"]
    inputs: List[str] = [
        "You should provide the data source, which is in form of datapipe:datapipe_key "
        "the datapipe_key should be extracted from the result of previous actions.",
        "the analysis type which is one of **average**, **sum**, or **trend**.",
    ]
    outputs: List[str] = [
        (
            "Returns the same structure as data input. For example if the provided data is the output of affect_activity_get,"
            "The same keys as affect_activity_get will be returned."
        )
    ]
    # False if the output should directly passed back to the planner.
    # True if it should be stored in datapipe
    output_type: bool = True

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        try:
            df = pd.read_json(
                StringIO(inputs[0]["data"].strip()), orient="records"
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return json.loads(
                '{"Data": "No data for the selected date(s)!"}'
            )
        if df.empty:
            return json.loads(
                '{"Data": "No data for the selected date(s)!"}'
            )
        analysis_type = inputs[1].strip()
        if analysis_type == "average":
            df = df.drop("date", axis=1)  # No average for date!
            df = df.mean().to_frame().T
        elif analysis_type == "sum":
            df = df.drop("date", axis=1)  # No sum for date!
            df = df.sum().to_frame().T
        elif analysis_type == "trend":
            df = self._calculate_slope(df)
        else:
            raise ValueError(
                "The input analysis type has not been defined!"
            )
        df = df.round(2)
        json_out = df.to_json(orient="records")
        return json_out
