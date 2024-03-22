from typing import Dict
from typing import Type

from tasks.affect import ActivityAnalysis
from tasks.affect import ActivityGet
from tasks.affect import PPGAnalysis
from tasks.affect import PPGGet
from tasks.affect import SleepAnalysis
from tasks.affect import SleepGet
from tasks.affect import StressAnalysis
from tasks.google_search import GoogleSearch
from tasks.google_translator import GoogleTranslate
from tasks.internals.ask_user import AskUser
from tasks.internals.audio_to_text import AudioToText
from tasks.nutritionix.calculate_food_risk_factor import (
    CalculateFoodRiskFactor,
)
from tasks.nutritionix.query_nutritionix import QueryNutritionix
from tasks.playwright import ExtractText
from tasks.run_python_code import RunPythonCode
from tasks.serpapi import SerpAPI
from tasks.task import BaseTask
from tasks.task_types import TaskType
from tasks.test_file import TestFile


TASK_TO_CLASS: Dict[TaskType, Type[BaseTask]] = {
    TaskType.SERPAPI: SerpAPI,
    TaskType.EXTRACT_TEXT: ExtractText,
    TaskType.AFFECT_SLEEP_GET: SleepGet,
    TaskType.AFFECT_ACTIVITY_GET: ActivityGet,
    TaskType.AFFECT_SLEEP_ANALYSIS: SleepAnalysis,
    TaskType.AFFECT_ACTIVITY_ANALYSIS: ActivityAnalysis,
    TaskType.GOOGLE_TRANSLATE: GoogleTranslate,
    TaskType.TEST_FILE: TestFile,
    TaskType.RUN_PYTHON_CODE: RunPythonCode,
    TaskType.PPG_GET: PPGGet,
    TaskType.PPG_ANALYSIS: PPGAnalysis,
    TaskType.STRESS_ANALYSIS: StressAnalysis,
    TaskType.QUERY_NUTRITIONIX: QueryNutritionix,
    TaskType.CALCULATE_FOOD_RISK_FACTOR: CalculateFoodRiskFactor,
    TaskType.GOOGLE_SEARCH: GoogleSearch,
}

INTERNAL_TASK_TO_CLASS: Dict[TaskType, Type[BaseTask]] = {
    TaskType.ASK_USER: AskUser,
    TaskType.AUDIO_TO_TEXT: AudioToText,
}
