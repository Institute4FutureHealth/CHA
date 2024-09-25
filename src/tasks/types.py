from typing import Dict
from typing import Type

from affect import ActivityAnalysis
from affect import ActivityGet
from affect import PPGAnalysis
from affect import PPGGet
from affect import SleepAnalysis
from affect import SleepGet
from affect import StressAnalysis
from ask_user import AskUser
from extract_text import ExtractText
from google_search import GoogleSearch
from google_translator import GoogleTranslate
from nutritionix.calculate_food_risk_factor import (
    CalculateFoodRiskFactor,
)
from nutritionix.query_nutritionix import QueryNutritionix
from run_python_code import RunPythonCode
from serpapi import SerpAPI
from task import BaseTask
from task_types import TaskType
from test_file import TestFile


TASK_TO_CLASS: Dict[TaskType, Type[BaseTask]] = {
    TaskType.SERPAPI: SerpAPI,
    TaskType.EXTRACT_TEXT: ExtractText,
    TaskType.AFFECT_SLEEP_GET: SleepGet,
    TaskType.AFFECT_ACTIVITY_GET: ActivityGet,
    TaskType.AFFECT_SLEEP_ANALYSIS: SleepAnalysis,
    TaskType.AFFECT_ACTIVITY_ANALYSIS: ActivityAnalysis,
    TaskType.GOOGLE_TRANSLATE: GoogleTranslate,
    TaskType.ASK_USER: AskUser,
    TaskType.TEST_FILE: TestFile,
    TaskType.RUN_PYTHON_CODE: RunPythonCode,
    TaskType.PPG_GET: PPGGet,
    TaskType.PPG_ANALYSIS: PPGAnalysis,
    TaskType.STRESS_ANALYSIS: StressAnalysis,
    TaskType.QUERY_NUTRITIONIX: QueryNutritionix,
    TaskType.CALCULATE_FOOD_RISK_FACTOR: CalculateFoodRiskFactor,
    TaskType.GOOGLE_SEARCH: GoogleSearch,
}
