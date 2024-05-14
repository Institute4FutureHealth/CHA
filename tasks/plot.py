import uuid
from io import StringIO
from typing import Any
from typing import List

import matplotlib.pyplot as plt
import pandas as pd

from tasks.task import BaseTask
from tasks.task import OutputType

# import seaborn as sns


class PlotTask(BaseTask):
    """
    **Description:**

        This task generates plots based on the input data and plot type.
    """

    name: str = "plot_task"
    chat_name: str = "Plot"
    description: str = (
        "When a request for creating a visual representations of data is received, call this visualization tool."
        "This tool is specifically designed to ensures accurate visualizations "
        "of data spanning various timeframes or categories. For instance, it can aggregate data over a year to highlight "
        "annual trends or examine it by month for more detailed insights. It's equipped to execute multiple times for "
        "segmented analysis, catering to the specific temporal needs of the user."
    )
    dependencies: List[str] = []  # uncertain, no dependencies?
    inputs: List[str] = [
        "You should provide the data source, which is in form of datapipe: datapipe_key."
        "The datapipe_key should be extracted from one of the existing datapipe_key."
        "Data should be derived from an uploaded file that contains the data needed to be ploted.",
        "Plot_type can be chosen based on what the user requires or the context implies, which can be among the following options"
        ": line, bar, scatter, histogram",
        "Time is the time series data that will be used as the x-axis in the plot. You should find the column name of the time series"
        " data from the data source.",
        "Plot_data is the data that will be used as the y-axis in the plot. You should find the column name of the plot data from the data source.",
    ]
    """
    "data: str = 'path/to/data.csv'",
    "plot_type: str = 'line'",
    "time: str = 'time_column'",
    "plot_data: str = 'plot_data_column'"
    """
    outputs: List[str] = [
        "returns a png file of the generated plot image, "
    ]
    executor_task: bool = False  # uncertain, no executor task?
    output_type: OutputType = OutputType.METADATA

    def _execute(self, inputs: List[Any] = None) -> str:
        try:
            df = pd.read_json(
                StringIO(inputs[0]["data"]), orient="records"
            )
        except Exception as e:
            print(f"An error occurred while reading the data: {e}")
            raise ValueError(
                "Failed to parse the input data. Please check the format."
            )
        # if data does not exist, don't call it, add checks: 1) array? 2) inputs[2] and inputs[3] are in the
        if df.empty:
            return self._create_plot(df, "empty", "Empty", "Empty")

        # df = pd.DataFrame.from_dict(inputs[0]['data'])
        # df = pd.DataFrame([inputs[0]['data']], index=[0])
        plot_type = inputs[1]
        x_axis = inputs[2]
        y_axis = inputs[3]

        if x_axis not in df.columns or y_axis not in df.columns:
            raise ValueError(
                f"Required columns '{x_axis}' or '{y_axis}' are missing in the data."
            )

        if plot_type not in [
            "line",
            "bar",
            "scatter",
            "histogram",
        ]:  # plot type data
            raise ValueError(
                f"Plot type '{plot_type}' is not supported."
            )

        return self._create_plot(df, plot_type, x_axis, y_axis)

    def _create_plot(self, df, plot_type, x_axis, y_axis):
        if plot_type == "empty":
            plt.figure()
            plt.text(
                0.5,
                0.5,
                "No Data Available",
                horizontalalignment="center",
                verticalalignment="center",
            )
        else:
            if plot_type == "line":
                plt.plot(df[x_axis], df[y_axis])
            elif plot_type == "bar":
                plt.bar(df[x_axis], df[y_axis])
            elif plot_type == "scatter":
                plt.scatter(df[x_axis], df[y_axis])
            elif plot_type == "histogram":
                plt.hist(df[y_axis])

        plt.xlabel(x_axis if plot_type != "empty" else "")
        plt.ylabel(y_axis if plot_type != "empty" else "")
        plt.title(
            f"{plot_type.capitalize()} Plot"
            if plot_type != "empty"
            else "Empty Plot"
        )

        filename = f"./data/{str(uuid.uuid4())}.png"
        plt.savefig(filename)
        plt.close()
        return filename

    def explain(self) -> str:
        return "This task generates a plot based on the input data and specified plot type."
