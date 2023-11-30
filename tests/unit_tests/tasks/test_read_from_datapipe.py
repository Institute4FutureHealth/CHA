import pytest
from pydantic import create_model

from datapipes.datapipe import DataPipe
from datapipes.datapipe_types import DatapipeType
from datapipes.initialize_datapipe import initialize_datapipe
from tasks.read_from_datapipe import ReadDataPipe


@pytest.fixture
def read_datapipe_task():
    return ReadDataPipe(
        datapipe=initialize_datapipe(datapipe=DatapipeType.MEMORY)
    )


def test_execute(read_datapipe_task):
    data_to_store = {
        "data": "test_data",
        "description": "test_description",
    }
    result = read_datapipe_task._execute([data_to_store])
    assert "test_data" in result
    assert "test_description" in result


def test_explain(read_datapipe_task):
    explanation = read_datapipe_task.explain()

    assert explanation == "This task is to read data from datapipe."
