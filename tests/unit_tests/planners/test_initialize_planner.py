from unittest.mock import patch

import pytest

from planners.planner import BasePlanner
from planners.planner_types import PlannerType
from llms.llm_types import LLMType
from tasks.initialize_task import initialize_task
from tasks.task import BaseTask
from tasks.task_types import TaskType
from planners.initialize_planner import initialize_planner
from pytest import raises
import os

from tasks.types import TASK_TO_CLASS

os.environ["OPENAI_API_KEY"] = "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"


# @pytest.fixture
# def openai_api_key():
#     return "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"


def test_initialize_planner_valid_types(get_serpapi_key):
    available_tasks = [TaskType.SERPAPI]
    tasks = {}
    for task in available_tasks:
        tasks[task.name] = initialize_task(task=task, serpapi_api_key=get_serpapi_key)

    # tasks = [TaskType.SERPAPI]
    llm_type = LLMType.OPENAI
    planner_type = PlannerType.ZERO_SHOT_REACT_PLANNER

    planner = initialize_planner(tasks=list(tasks.values()), llm=llm_type, planner=planner_type)

    assert planner is not None
    assert isinstance(planner, BasePlanner)


def test_initialize_planner_invalid_types(get_serpapi_key):
    available_tasks = [TaskType.SERPAPI]
    tasks = {}
    for task in available_tasks:
        tasks[task.name] = initialize_task(task=task, serpapi_api_key=get_serpapi_key)

    # tasks = [TaskType.SERPAPI]
    llm_type = LLMType.OPENAI
    planner_type = "InvalidPlannerType"

    with raises(ValueError, match="Got unknown planner type: InvalidPlannerType. Valid types are: dict_keys\(\[<PlannerType.ZERO_SHOT_REACT_PLANNER: 'zero_shot_react_planner'>\]\)"):
        initialize_planner(tasks=list(tasks.values()), llm=llm_type, planner=planner_type)

    llm_type = "InvalidLLMType"
    planner_type = PlannerType.ZERO_SHOT_REACT_PLANNER

    with raises(ValueError, match="Got unknown llm type: InvalidLLMType. Valid types are: dict_keys\(\[<LLMType.OPENAI: 'openai'>, <LLMType.ANTHROPIC: 'anthropic'>\]\)"):
        initialize_planner(tasks=list(tasks.values()), llm=llm_type, planner=planner_type)
