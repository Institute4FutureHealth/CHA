import json
from io import StringIO
from typing import Any
from typing import List
from typing import Optional

import pandas as pd

from tasks.affect.base import Affect
from tasks.task import OutputType


class StatisticalAnalysis(Affect):
    """
    **Description:**

        This task performs average, sum, or trend analysis on the provided raw data for specific types of data.
    """

    name: str = "statistical_analysis"
    chat_name: str = "StatisticalAnalysis"
    description: str = (
        "When a request for analysis of data is received (such as calculating averages, sums, or identifying trends), "
        "call this analysis tool. This tool is designed to handle complex data computations on various data records, "
        "ensuring precise and reliable results. Example: If the data spans a year and the user seeks an average data, "
        "this tool will calculate the yearly average. If monthly data is needed, this task should be called multiple times for each month."
    )
    dependencies: List[str] = []
    inputs: List[str] = [
        "You should provide the data source, which is in the form of datapipe:datapipe_key. "
        "The datapipe_key should be extracted from the result of previous actions.",
        "The analysis type which is one of **average**, **sum**, or **trend**.",
        "An optional parameter to specify columns to include in the analysis.",
        "The frequency for averaging in minutes (e.g., 1440 for daily, 10080 for weekly).",
    ]
    outputs: List[str] = [
        "Returns an array of JSON objects with the analyzed data. The structure of the output depends on the input data and analysis type.",
    ]
    output_type: OutputType = OutputType.DATAPIPE

    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        try:
            df = pd.read_json(
                StringIO(inputs[0]["data"].strip()), orient="records"
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return json.dumps(
                {"Data": "No data for the selected date(s)!"}
            )

        if df.empty:
            return json.dumps(
                {"Data": "No data for the selected date(s)!"}
            )

        analysis_type = inputs[1].strip()
        columns_to_include: Optional[List[str]] = (
            inputs[2].split(",") if len(inputs) > 2 else None
        )
        frequency = inputs[3] if len(inputs) > 3 else None

        if columns_to_include:
            df = df[columns_to_include]

        if frequency:
            frequency = int(
                frequency
            )  # Ensure frequency is an integer
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], unit="ms")
                df = df.set_index("date")
                df = df.resample(f"{frequency}T").mean().reset_index()

        if analysis_type == "average":
            df = df.mean().to_frame().T
        elif analysis_type == "sum":
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

    def _calculate_slope(self, df: pd.DataFrame) -> pd.DataFrame:
        trend_df = pd.DataFrame()
        for column in df.columns:
            if column != "date":
                trend_df[column] = [
                    self._linear_regression_slope(
                        df["date"], df[column]
                    )
                ]
        return trend_df

    def _linear_regression_slope(
        self, x: pd.Series, y: pd.Series
    ) -> float:
        n = len(x)
        sum_x = x.sum()
        sum_y = y.sum()
        sum_x_squared = (x**2).sum()
        sum_xy = (x * y).sum()
        slope = (n * sum_xy - sum_x * sum_y) / (
            n * sum_x_squared - sum_x**2
        )
        return slope
