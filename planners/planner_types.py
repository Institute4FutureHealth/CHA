from enum import Enum


class PlannerType(str, Enum):
    ZERO_SHOT_REACT_PLANNER = "zero_shot_react_planner"
    TREE_OF_THOUGHT = "tree_of_thought"
