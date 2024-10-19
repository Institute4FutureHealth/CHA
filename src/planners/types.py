from typing import Dict
from typing import Type

from planners import BasePlanner
from planners import PlannerType
from planners import TreeOfThoughtPlanner
from planners.react import ReActPlanner


PLANNER_TO_CLASS: Dict[PlannerType, Type[BasePlanner]] = {
    PlannerType.ZERO_SHOT_REACT_PLANNER: ReActPlanner,
    PlannerType.TREE_OF_THOUGHT: TreeOfThoughtPlanner,
}
