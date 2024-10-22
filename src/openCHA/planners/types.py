from typing import Dict
from typing import Type

from openCHA.planners import BasePlanner
from openCHA.planners import PlannerType
from openCHA.planners import TreeOfThoughtPlanner
from openCHA.planners.react import ReActPlanner


PLANNER_TO_CLASS: Dict[PlannerType, Type[BasePlanner]] = {
    PlannerType.ZERO_SHOT_REACT_PLANNER: ReActPlanner,
    PlannerType.TREE_OF_THOUGHT: TreeOfThoughtPlanner,
}
