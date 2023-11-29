import pytest

from datapipes.datapipe import DataPipe
from datapipes.datapipe_types import DatapipeType
from datapipes.initialize_datapipe import initialize_datapipe


@pytest.fixture
def fake_datapipe():
    return "This is a fake DataPipe object."


def test_initialize_datapipe_with_valid_type(fake_datapipe):
    result = initialize_datapipe(datapipe=DatapipeType.MEMORY, fake_datapipe=fake_datapipe)
    assert isinstance(result, DataPipe)


def test_initialize_datapipe_with_invalid_type():
    with pytest.raises(ValueError):
        initialize_datapipe(datapipe="InvalidType")


def test_with_default_type():
    memory_datapipe = initialize_datapipe(datapipe=DatapipeType.MEMORY)
    assert isinstance(memory_datapipe, DataPipe)
