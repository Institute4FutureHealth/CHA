from typing import Dict
from typing import Type

from tasks import AskUser
from tasks import BaseTask
from tasks import ExtractText
from tasks import GoogleSearch
from tasks import GoogleTranslate
from tasks import RunPythonCode
from tasks import SerpAPI
from tasks import TaskType
from tasks import TestFile
from tasks.affect import ActivityAnalysis
from tasks.affect import ActivityGet
from tasks.affect import PPGAnalysis
from tasks.affect import PPGGet
from tasks.affect import SleepAnalysis
from tasks.affect import SleepGet
from tasks.affect import StressAnalysis
from tasks.nutritionix import (
    CalculateFoodRiskFactor,
)
from tasks.nutritionix import QueryNutritionix


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
