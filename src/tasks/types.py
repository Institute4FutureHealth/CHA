from typing import Dict
from typing import Type

from tasks.affect import ActivityAnalysis
from tasks.affect import ActivityGet
from tasks.affect import PPGAnalysis
from tasks.affect import PPGGet
from tasks.affect import SleepAnalysis
from tasks.affect import SleepGet
from tasks.affect import StressAnalysis
from tasks.ask_user import AskUser
from tasks.google_translator import GoogleTranslate
from tasks.playwright.click import Click
from tasks.playwright import CurrentWebPage
from tasks.playwright import ExtractHyperlinks
from tasks.playwright import ExtractText
from tasks.playwright import GetElements
from tasks.playwright import Navigate
from tasks.playwright import NavigateBack
from tasks.read_from_datapipe import ReadDataPipe
from tasks.run_python_code import RunPythonCode
from tasks.serpapi import SerpAPI
from tasks.task import BaseTask
from tasks.task_types import TaskType
from tasks.test_file import TestFile


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
    TaskType.AFFECT_SLEEP_ANALYSIS: SleepAnalysis,
    TaskType.AFFECT_ACTIVITY_ANALYSIS: ActivityAnalysis,
    TaskType.GOOGLE_TRANSLATE: GoogleTranslate,
    TaskType.ASK_USER: AskUser,
    TaskType.TEST_FILE: TestFile,
    TaskType.READ_FROM_DATAPIPE: ReadDataPipe,
    TaskType.RUN_PYTHON_CODE: RunPythonCode,
    TaskType.PPG_GET: PPGGet,
    TaskType.PPG_ANALYSIS: PPGAnalysis,
    TaskType.STRESS_ANALYSIS: StressAnalysis,
}
