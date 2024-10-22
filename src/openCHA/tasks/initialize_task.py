from typing import Any

from openCHA.datapipes import DataPipe
from openCHA.tasks import BaseTask
from openCHA.tasks import TASK_TO_CLASS


def initialize_task(task: str = "serpapi", **kwargs: Any) -> BaseTask:
    """
    Initialize a task based on the provided task name.

    Args:
        task (str): The name of the task to initialize.
        **kwargs (Any): Additional keyword arguments for customizing task initialization.
    Return:
        BaseTask: An instance of the initialized task.
    Raise:
        ValueError: If the provided task name is unknown.



    Example:
        .. code-block:: python



    """

    if task not in TASK_TO_CLASS:
        raise ValueError(
            f"Got unknown planner type: {task}. "
            f"Valid types are: {TASK_TO_CLASS.keys()}."
        )

    task_cls = TASK_TO_CLASS[task]
    task = task_cls(**kwargs)
    return task
