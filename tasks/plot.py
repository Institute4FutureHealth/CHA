from typing import List, Any
import matplotlib.pyplot as plt
import pandas as pd
import uuid

# import seaborn as sns

from tasks.task import BaseTask
from tasks.task import OutputType

class PlotTask(BaseTask):
    """
    **Description:**

        This task generates plots based on the input data and plot type.

    **Attributes:**
    
        - name (str): Name of the task.
        - chat_name (str): How the task will be referred to in chat.
        - description (str): A brief description of what the task does.
        - dependencies (List[str]): List of dependencies required by the task.
        - inputs (List[str]): Inputs required to execute the task.
        - outputs (List[str]): Outputs produced by the task.
        - executor_task (bool): Whether this is an executor task.
        - output_type (OutputType): The output type of the task.
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
    dependencies: List[str] = [] # uncertain, no dependencies?
    inputs: List[str] = [
        "You should provide the data source, which is in form of datapipe: datapipe_key."
        "The datapipe_key should be extracted from one of the existing datapipe_key."
        "Data should be derived from an uploaded file that contains the data needed to be ploted.",
        "Plot_type can be chosen based on what the user requires or the context implies, which can be among the following options: line, bar, scatter, histogram.",
        "Time is the time series data that will be used as the x-axis in the plot. You should find the column name of the time series data from the data source.",
        "Plot_data is the data that will be used as the y-axis in the plot. You should find the column name of the plot data from the data source."
    ]
    '''
    "data: str = 'path/to/data.csv'",
    "plot_type: str = 'line'",
    "time: str = 'time_column'",
    "plot_data: str = 'plot_data_column'"
    '''
    outputs: List[str] = [
        "returns a png file of the generated plot image, "
    ]
    executor_task: bool = False # uncertain, no executor task?
    output_type: OutputType = OutputType.METADATA

    def _execute(self, inputs: List[Any] = None) -> str:
        df = pd.read_json(inputs[0])
        plot_type = inputs[1]
        x_axis = inputs[2]
        y_axis = inputs[3]

        if plot_type == "line":
            plt.plot(df[x_axis], df[y_axis])
        elif plot_type == "bar":
            plt.bar(df[x_axis], df[y_axis])
        elif plot_type == "scatter":
            plt.scatter(df[x_axis], df[y_axis])
        elif plot_type == "histogram":
            plt.hist(df[y_axis])

        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title(f'{plot_type.capitalize()} Plot')

        filename = f"./data/{str(uuid.uuid4())}.png"
        plt.savefig(filename)
        plt.close()
        return filename

    def explain(self) -> str:
        return "This task generates a plot based on the input data and specified plot type."
