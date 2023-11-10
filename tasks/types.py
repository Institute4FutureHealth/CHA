from typing import Dict, Type, Union

from tasks.task_types import TaskType
from tasks.task import BaseTask
from tasks.serpapi import SerpAPI
from tasks.affect import *
from tasks.playwright import *


TASK_TO_CLASS: Dict[TaskType, Type[BaseTask]] = {
  TaskType.SERPAPI: SerpAPI,
  TaskType.CLICK: Click,
  TaskType.GET_CURRENT_PAGE: CurrentWebPage,
  TaskType.EXTRACT_HYPERLINKS: ExtractHyperlinks,
  TaskType.EXTRACT_TEXT: ExtractText,
  TaskType.GET_ELEMENTS: GetElements,
  TaskType.NAVIGATE_BACK: NavigateBack,
  TaskType.NAVIGATE: Navigate,
  TaskType.AFFECT_SLEEP: SleepAVG
}
