from typing import Any
from typing import List

from openCHA.llms import BaseLLM
from openCHA.llms import LLM_TO_CLASS
from openCHA.llms import LLMType
from openCHA.planners import BasePlanner
from openCHA.planners import PLANNER_TO_CLASS
from openCHA.planners import PlannerType
from openCHA.tasks import BaseTask


def initialize_planner(
    tasks: List[BaseTask] = None,
    llm: str = LLMType.OPENAI,
    planner: str = PlannerType.TREE_OF_THOUGHT,
    **kwargs: Any,
) -> BasePlanner:
    """
    Initialize a planner with specified tasks, language model type, and planner type.

    Args:
        tasks (List[BaseTask]): List of tasks to be associated with the planner.
        llm (str): Language model type.
        planner (str): Planner type.
        **kwargs (Any): Additional keyword arguments.
    Return:
        BasePlanner: Initialized planner instance.
    Raise:
        ValueError: If the specified planner or language model type is not recognized.



    Example:
        .. code-block:: python

            from openCHA.planners import PlannerType
            from openCHA.llms import LLMType
            from openCHA.tasks import TaskType
            planner = initialize_planner(tasks=[TaskType.SERPAPI], llm=LLMType.OPENAI, planner=PlannerType.ZERO_SHOT_REACT_PLANNER)

    """
    if tasks is None:
        tasks = []

    if planner not in PLANNER_TO_CLASS:
        raise ValueError(
            f"Got unknown planner type: {planner}. "
            f"Valid types are: {PLANNER_TO_CLASS.keys()}."
        )

    if llm not in LLM_TO_CLASS:
        raise ValueError(
            f"Got unknown llm type: {llm}. "
            f"Valid types are: {LLM_TO_CLASS.keys()}."
        )

    planner_cls = PLANNER_TO_CLASS[planner]
    llm_model = LLM_TO_CLASS[llm]()
    planner = planner_cls(llm_model=llm_model, available_tasks=tasks)
    return planner
