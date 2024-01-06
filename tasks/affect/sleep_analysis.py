from io import StringIO
from typing import Any
from typing import List

import pandas as pd

from tasks.affect.base import Affect


class SleepAnalysis(Affect):
    """
    **Description:**

        This tasks performs average, sum, or trend analysis on the provided raw sleep affect data for specific patient.
    """

    name: str = "affect_sleep_analysis"
    chat_name: str = "AffectSleepAnalysis"
    description: str = (
        "When a request for analysis of sleep data is received (such as calculating averages, sums, or identifying trends), "
        "call this analysis tool. This tool is specifically designed to handle complex data computations on sleep data records, "
        "ensuring precise and reliable results. Example: If the data spans a year and the user seeks an average sleep data, "
        "this tool will calculate the yearly average."
    )
    dependencies: List[str] = ["affect_sleep_get"]
    inputs: List[str] = [
        "You should provide the data source, which is in form of datapipe:datapipe_key "
        "the datapipe_key should be extracted from the result of previous actions.",
        "the analysis type which is one of **average** or **trend**.",
    ]
    outputs: List[str] = [
        (
            "Returns the same structure as data input. For example if the provided data is the output of affect_sleep_get,"
            "The same keys as affect_sleep_get will be returned."
        )
    ]
    # False if the output should directly passed back to the planner.
    # True if it should be stored in datapipe
    output_type: bool = True

    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        df = pd.read_json(
            StringIO(inputs[0]["data"].strip()), orient="records"
        )
        analysis_type = inputs[1].strip()
        if analysis_type == "average":
            df = df.drop("date", axis=1)  # No average for date!
            df = df.mean().to_frame().T
        elif analysis_type == "trend":
            df = self._calculate_slope(df)
        else:
            raise ValueError(
                "The input analysis type has not been defined!"
            )
        df = df.round(2)
        json_out = df.to_json(orient="records")
        return json_out
