import pytest

from llms import LLMType
from planners import initialize_planner
from planners import PlannerType
from planners import Action
from planners import PlanFinish
from tasks import initialize_task
from tasks import TaskType


@pytest.fixture
def react_planner(get_serpapi_key):
    task_name = TaskType.SERPAPI
    task = initialize_task(
        task=task_name, serpapi_api_key=get_serpapi_key
    )
    tasks = {task.name: task}
    llm_type = LLMType.OPENAI
    planner_type = PlannerType.ZERO_SHOT_REACT_PLANNER

    planner = initialize_planner(
        tasks=list(tasks.values()), llm=llm_type, planner=planner_type
    )

    return planner


def test_parse_with_valid_query(react_planner):
    query1 = f"""
        Thought: Think about the question
        Action: {TaskType.SERPAPI}
        Action Inputs: meal_plan
    """

    query2 = """
        Thought: I now know the final answer.
        Final Answer: You should have a balanced diet with more vegetables.
    """

    query3 = """
        Thought: Think about the question
        Observation: Eat more vegetables.
        Thought: Final reasoning or 'I now know the final answer'.
        Final Answer: You should have a balanced diet with more vegetables.
    """

    result = react_planner.parse(query1)
    assert isinstance(result, list)
    assert isinstance(result[0], Action)
    assert result[0].task == TaskType.SERPAPI
    assert result[0].task_input == "meal_plan\n"

    result = react_planner.parse(query2)
    assert isinstance(result, list)
    assert isinstance(result[0], PlanFinish)
    assert (
        result[0].response
        == "You should have a balanced diet with more vegetables."
    )

    result = react_planner.parse(query3)
    assert isinstance(result, list)
    assert isinstance(result[0], PlanFinish)
    assert (
        result[0].response
        == "You should have a balanced diet with more vegetables."
    )


def test_parse_with_invalid_query(react_planner):
    query1 = """
        Thought: Think about the question
        Observation: Eat more vegetables.
        Thought: Final reasoning or 'I now know the final answer'.
    """

    with pytest.raises(
        ValueError,
        match="Invalid Format: Missing 'Action:' or 'Final Answer' after 'Thought:'",
    ):
        react_planner.parse(query1)

    query2 = """
        Thought: Think about the question
        Action:
    """

    with pytest.raises(
        ValueError,
        match="Invalid Format: Missing 'Action:' or 'Final Answer' after 'Thought:'",
    ):
        react_planner.parse(query2)

    query3 = f"""
        Thought: Think about the question
        Action: {TaskType.SERPAPI}
        Action Inputs: meal_plan
        Observation: Eat more vegetables.
        Thought: Final reasoning or 'I now know the final answer'.
        Final Answer: You should have a balanced diet with more vegetables.
    """

    with pytest.raises(
        ValueError,
        match="Parsing the output produced both a final answer and a parse-able action.",
    ):
        react_planner.parse(query3)
