import pytest

from tasks import initialize_task
from tasks import TaskType
from tasks import TASK_TO_CLASS


def test_initialize_task_with_known_task():
    task_name = TaskType.SERPAPI
    kwargs = {}

    result = initialize_task(task=task_name, **kwargs)

    assert isinstance(result, TASK_TO_CLASS[task_name])


def test_initialize_task_with_unknown_task():
    unknown_task_name = "unknown_task"
    kwargs = {"key1": "value1", "key2": "value2"}

    with pytest.raises(
        ValueError,
        match=f"Got unknown planner type: {unknown_task_name}\\..*",
    ):
        initialize_task(task=unknown_task_name, **kwargs)
