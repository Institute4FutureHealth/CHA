from typing import Dict
from typing import Type

from planners.planner import BasePlanner
from planners.planner_types import PlannerType
from planners.react.base import ReActPlanner
from planners.tree_of_thought import TreeOfThoughtPlanner


PLANNER_TO_CLASS: Dict[PlannerType, Type[BasePlanner]] = {
    PlannerType.ZERO_SHOT_REACT_PLANNER: ReActPlanner,
    PlannerType.TREE_OF_THOUGHT: TreeOfThoughtPlanner,
}
