from typing import Dict
from typing import Type

from openCHA.tasks import AskUser
from openCHA.tasks import BaseTask
from openCHA.tasks import ExtractText
from openCHA.tasks import GoogleSearch
from openCHA.tasks import GoogleTranslate
from openCHA.tasks import RunPythonCode
from openCHA.tasks import SerpAPI
from openCHA.tasks import TaskType
from openCHA.tasks import TestFile
from openCHA.tasks.affect import ActivityAnalysis
from openCHA.tasks.affect import ActivityGet
from openCHA.tasks.affect import PPGAnalysis
from openCHA.tasks.affect import PPGGet
from openCHA.tasks.affect import SleepAnalysis
from openCHA.tasks.affect import SleepGet
from openCHA.tasks.affect import StressAnalysis
from openCHA.tasks.nutritionix import (
    CalculateFoodRiskFactor,
)
from openCHA.tasks.nutritionix import QueryNutritionix


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
