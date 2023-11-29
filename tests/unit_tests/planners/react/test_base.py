import os

import pytest

from llms.llm_types import LLMType
from planners.initialize_planner import initialize_planner
from planners.planner_types import PlannerType
from planners.react.base import ReActPlanner, Action, PlanFinish
from tasks.initialize_task import initialize_task
from tasks.task_types import TaskType


os.environ["OPENAI_API_KEY"] = "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"


@pytest.fixture
def react_planner(get_serpapi_key):
    task = TaskType.SERPAPI
    tasks = {task.name: initialize_task(task=task, serpapi_api_key=get_serpapi_key)}

    llm_type = LLMType.OPENAI
    planner_type = PlannerType.ZERO_SHOT_REACT_PLANNER

    planner = initialize_planner(tasks=list(tasks.values()), llm=llm_type, planner=planner_type)

    return ReActPlanner(llm_model=planner.llm_model)


def test_plan_with_previous_actions(react_planner):
    query = "How can I improve my health?"
    history = "User: What should I eat?\nAssistant: You should have a balanced diet."
    meta = "No specific metadata for this test."
    previous_actions = [Action("DietRecommendationTool", "meal_plan", "Eat more vegetables.", ""),
                        Action("ExerciseTool", "exercise_plan", "Go for a 30-minute walk.", "")]

    result = react_planner.plan(query, history, meta, previous_actions, use_history=True)

    assert isinstance(result, list)
    assert all(isinstance(action, (Action, PlanFinish)) for action in result)


def test_plan_without_previous_actions(react_planner):
    query = "How can I improve my health?"
    history = "User: What should I eat?\nAssistant: You should have a balanced diet."
    meta = "No specific metadata for this test."

    result = react_planner.plan(query, history, meta, use_history=True)

    assert isinstance(result, list)
    assert all(isinstance(action, (Action, PlanFinish)) for action in result)


def test_parse_with_valid_query(react_planner):
    query = """
        Thought: Think about the question
        Action: DietRecommendationTool
        Action Inputs: meal_plan
        Observation: Eat more vegetables.
        Thought: Final reasoning or 'I now know the final answer'.
        Final Answer: You should have a balanced diet with more vegetables.
    """

    result = react_planner.parse(query)

    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], Action)
    assert isinstance(result[1], PlanFinish)


def test_parse_with_invalid_query(react_planner):
    query = """
        Thought: Think about the question
        Observation: Eat more vegetables.
        Thought: Final reasoning or 'I now know the final answer'.
        Final Answer: You should have a balanced diet with more vegetables.
    """

    with pytest.raises(ValueError, match="Invalid Format: Missing 'Action:' or 'Final Answer' after 'Thought:'"):
        result = react_planner.parse(query)

