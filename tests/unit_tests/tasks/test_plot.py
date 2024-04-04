import json
import os

import pytest

from tasks.plot import PlotTask

def test_plot_task_execute():
    # Sample data for plotting
    data = json.dumps([
        {"x": 1, "y": 2},
        {"x": 2, "y": 3},
        {"x": 3, "y": 5},
        {"x": 4, "y": 7},
        {"x": 5, "y": 11},
    ])
    
    plot_task = PlotTask()

    # Temporary file path for the plot image
    plot_filename = "temp_plot.png"

    # Run the plot task
    result_filename = plot_task._execute([data, "line", "x", "y"])

    # Check that the file was created
    assert os.path.exists(result_filename)

    # Clean up the file after the test
    # if os.path.exists(plot_filename):
    #     os.remove(plot_filename)
