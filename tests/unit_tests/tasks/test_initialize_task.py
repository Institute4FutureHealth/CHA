import os

import pytest
from unittest.mock import MagicMock, patch
from tasks.task import BaseTask
from tasks.initialize_task import initialize_task


os.environ["SERPAPI_API_KEY"] = "test key for serpapi"


def test_initialize_task_with_known_task():
    task_name = "serpapi"
    kwargs = {"serpapi_api_key": "test key for serpapi"}

    result = initialize_task(task=task_name, **kwargs)

    assert isinstance(result, BaseTask)


def test_initialize_task_with_unknown_task():

    unknown_task_name = "unknown_task"
    kwargs = {"key1": "value1", "key2": "value2"}

    with pytest.raises(ValueError, match=f"Got unknown planner type: {unknown_task_name}\\..*"):
        initialize_task(task=unknown_task_name, **kwargs)
