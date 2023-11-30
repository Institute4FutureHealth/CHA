import pytest
from pytest import raises

from llms.llm_types import LLMType
from planners.initialize_planner import initialize_planner
from planners.planner import BasePlanner
from planners.planner_types import PlannerType
from tasks.initialize_task import initialize_task
from tasks.task import BaseTask
from tasks.task_types import TaskType
from tasks.types import TASK_TO_CLASS


def test_initialize_planner_valid_types(get_serpapi_key):
    available_tasks = [TaskType.SERPAPI]
    tasks = {}
    for task in available_tasks:
        tasks[task.name] = initialize_task(
            task=task, serpapi_api_key=get_serpapi_key
        )

    # tasks = [TaskType.SERPAPI]
    llm_type = LLMType.OPENAI
    planner_type = PlannerType.ZERO_SHOT_REACT_PLANNER

    planner = initialize_planner(
        tasks=list(tasks.values()), llm=llm_type, planner=planner_type
    )

    assert planner is not None
    assert isinstance(planner, BasePlanner)


def test_initialize_planner_invalid_types(get_serpapi_key):
    available_tasks = [TaskType.SERPAPI]
    tasks = {}
    for task in available_tasks:
        tasks[task.name] = initialize_task(
            task=task, serpapi_api_key=get_serpapi_key
        )

    # tasks = [TaskType.SERPAPI]
    llm_type = LLMType.OPENAI
    planner_type = "InvalidPlannerType"

    with raises(
        ValueError,
    ):
        initialize_planner(
            tasks=list(tasks.values()),
            llm=llm_type,
            planner=planner_type,
        )

    llm_type = "InvalidLLMType"
    planner_type = PlannerType.ZERO_SHOT_REACT_PLANNER

    with raises(
        ValueError,
    ):
        initialize_planner(
            tasks=list(tasks.values()),
            llm=llm_type,
            planner=planner_type,
        )
