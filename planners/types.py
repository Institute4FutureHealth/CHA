from typing import Dict, Type, Union

from planners.planner_types import PlannerType
from planners.planner import BasePlanner
from planners.react.base import ReActPlanner


PLANNER_TO_CLASS: Dict[PlannerType, Type[BasePlanner]] = {
  PlannerType.ZERO_SHOT_REACT_PLANNER: ReActPlanner
}
