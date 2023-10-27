from typing import Dict, Type, Union

from tasks.task_types import TaskType
from tasks.task import BaseTask
from tasks.serpapi import SerpAPI


TASK_TO_CLASS: Dict[TaskType, Type[BaseTask]] = {
  TaskType.SERPAPI: SerpAPI
}
