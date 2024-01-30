import pytest

from src.datapipes.datapipe_types import DatapipeType
from src.datapipes import initialize_datapipe


def test_memory_datapipe_store_and_retrieve():
    # Initialize a Memory DataPipe
    memory_datapipe = initialize_datapipe(
        datapipe=DatapipeType.MEMORY
    )

    # Data to be stored
    sample_data = {"key": "value"}

    # Store data and get the key
    key = memory_datapipe.store(sample_data)

    # Retrieve data using the key
    retrieved_data = memory_datapipe.retrieve(key)

    # Check if the retrieved data matches the stored data
    assert retrieved_data == sample_data


def test_memory_datapipe_retrieve_nonexistent_key():
    # Initialize a Memory DataPipe
    memory_datapipe = initialize_datapipe(
        datapipe=DatapipeType.MEMORY
    )

    # Attempt to retrieve data using a nonexistent key
    nonexistent_key = "nonexistent_key"

    # Check if ValueError is raised
    with pytest.raises(
        ValueError,
        match=f"The data with the key {nonexistent_key} does not exist.",
    ):
        memory_datapipe.retrieve(nonexistent_key)
