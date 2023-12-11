import json
from typing import Any
from typing import List

import pytest

from datapipes.datapipe_types import DatapipeType
from datapipes.initialize_datapipe import initialize_datapipe
from tasks.task import BaseTask


class SampleTask(BaseTask):
    name: str = "sample_task"
    chat_name: str = "SampleTask"
    description: str = "sample task"
    inputs: List[str] = []
    dependencies: List[str] = []

    def _execute(self, inputs: List[Any]) -> str:
        return ""


@pytest.fixture
def datapipe():
    datapipe = initialize_datapipe(datapipe=DatapipeType.MEMORY)
    return datapipe


@pytest.fixture
def sample_task(datapipe):
    kwargs = {"datapipe": datapipe}
    task = SampleTask(**kwargs)
    return task


def test_parse_input_simple(sample_task):
    input_args = "input1"
    inputs = sample_task._parse_input(input_args=input_args)

    assert len(inputs) == 1
    assert inputs[0] == "input1"

    input_args = "input1,input2"
    inputs = sample_task._parse_input(input_args=input_args)

    assert len(inputs) == 2
    assert inputs[0] == "input1"
    assert inputs[1] == "input2"

    input_args = "\ninput1 , \ninput2"
    inputs = sample_task._parse_input(input_args=input_args)

    assert len(inputs) == 2
    assert inputs[0] == "input1"
    assert inputs[1] == "input2"


def test_parse_input_with_datapipe(sample_task, datapipe):
    data = json.dumps(
        {
            "data": "sample data",
            "description": "sample description",
        }
    )
    key = datapipe.store(data)
    input_args = f"datapipe:{key},input2"
    inputs = sample_task._parse_input(input_args=input_args)
    assert len(inputs) == 2
    assert "sample data" in inputs[0]["data"]
    assert inputs[1] == "input2"


def test_post_execute_direct_return(sample_task):
    result = "this is the task sample output"
    assert result == sample_task._post_execute(result=result)


def test_post_execute_store_in_datapipe(sample_task):
    result = "this is the task sample output"
    sample_task.output_type = True
    assert "datapipe:" in sample_task._post_execute(result=result)


def test_get_dict(sample_task):
    assert isinstance(sample_task.get_dict(), str)


def test_validate_inputs(sample_task):
    sample_task.inputs = ["input 1", "input 2"]

    inputs = []
    assert not sample_task._validate_inputs(inputs)

    inputs = ["input 1"]
    assert not sample_task._validate_inputs(inputs)

    inputs = ["input 1", "input 2"]
    assert sample_task._validate_inputs(inputs)
