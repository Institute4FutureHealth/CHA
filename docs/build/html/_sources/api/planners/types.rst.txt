Types
=====




Planner Types
-------------



This code defines an enumeration class called PlannerType, which inherits from the Enum class provided by the enum module.


.. code:: python

    from enum import Enum 

    class PlannerType(str, Enum):
    ZERO_SHOT_REACT_PLANNER = "zero-shot-react-planner"



|


Types
-----


This code defines a dictionary called PLANNER_TO_CLASS that maps PlannerType values to corresponding planner classes.


.. code:: python

    from typing import Dict, Type, Union

    from planners.planner_types import PlannerType
    from planners.planner import BasePlanner
    from planners.react.base import ReActPlanner


    PLANNER_TO_CLASS: Dict[PlannerType, Type[BasePlanner]] = {
    PlannerType.ZERO_SHOT_REACT_PLANNER: ReActPlanner
    }













