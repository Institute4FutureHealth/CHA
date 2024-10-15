import pytest

from orchestrator import Action
from orchestrator import Orchestrator


@pytest.fixture
def sample_orchestrator():
    return Orchestrator.initialize()


def test_initialize():
    orchestrator = Orchestrator.initialize()
    assert orchestrator is not None
    assert isinstance(orchestrator, Orchestrator)


def test_process_meta(sample_orchestrator):
    result = sample_orchestrator.process_meta()
    assert result is False


def test_execute_task(sample_orchestrator):
    action = Action("example_task", "example_input", "", "")
    result, return_direct = sample_orchestrator.execute_task(action)
    assert isinstance(result, str)
    assert isinstance(return_direct, bool)


def test_planner_generate_prompt(sample_orchestrator):
    query = "example_query"
    result = sample_orchestrator.planner_generate_prompt(query)
    assert isinstance(result, str)


def test_response_generator_generate_prompt(sample_orchestrator):
    final_response = "example_final_response"
    history = "example_history"
    meta = ["example_meta_1", "example_meta_2"]
    previous_actions = [
        Action("example_task", "example_input", "sample_result", "")
    ]
    use_history = True
    result = sample_orchestrator.response_generator_generate_prompt(
        final_response=final_response,
        history=history,
        meta=meta,
        previous_actions=previous_actions,
        use_history=use_history,
    )
    assert isinstance(result, str)


# def test_plan(sample_orchestrator):
#     query = "example_query"
#     history = "example_history"
#     meta = ["example_meta_1", "example_meta_2"]
#     previous_actions = [Action("example_task", "example_input", "sample_result", "")]
#     use_history = True
#     result = sample_orchestrator.plan(query=query, history=history, meta=meta, previous_actions=previous_actions, use_history=use_history)
#     assert isinstance(result, list)


def test_generate_final_answer(sample_orchestrator):
    query = "example_query"
    thinker = "example_thinker"
    result = sample_orchestrator.generate_final_answer(
        query=query, thinker=thinker
    )
    assert isinstance(result, str)


# def test_run(sample_orchestrator):
#     query = "example_query"
#     meta = ["example_meta_1", "example_meta_2"]
#     history = "example_history"
#     use_history = True
#     result, previous_actions = sample_orchestrator.run(query=query, meta=meta, history=history, use_history=use_history)
#     assert isinstance(result, str)
#     assert isinstance(previous_actions, list)
