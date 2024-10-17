import pytest
from datapipes import DatapipeType
from datapipes import initialize_datapipe
from tasks import ReadDataPipe


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
