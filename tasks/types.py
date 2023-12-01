from typing import Dict, Type, Union

from tasks.task_types import TaskType
from tasks.task import BaseTask
from tasks.serpapi import SerpAPI
from tasks.affect import *
from tasks.google_translator import GoogleTranslate
from tasks.ask_user import AskUser
from tasks.test_file import TestFile
from tasks.read_from_datapipe import ReadDataPipe
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
  TaskType.AFFECT_SLEEP_GET: SleepGet,
  TaskType.AFFECT_ACTIVITY_GET: ActivityGet,
  TaskType.AFFECT_PPG_GET: PpgGet,
  TaskType.AFFECT_SLEEP_ANALYSIS: SleepAnalysis,
  TaskType.AFFECT_ACTIVITY_ANALYSIS: ActivityAnalysis,
  TaskType.AFFECT_PPG_ANALYSIS: PpgAnalysis,
  TaskType.GOOGLE_TRANSLATE: GoogleTranslate,
  TaskType.ASK_USER: AskUser,
  TaskType.TEST_FILE: TestFile,
  TaskType.READ_FROM_DATAPIPE: ReadDataPipe
}
