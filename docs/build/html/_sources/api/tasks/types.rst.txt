Types
=====




Tasks Types
-----------




This code defines an enumeration class named TaskType using the Enum module in Python. 
Enums are a way to create named constant values that represent distinct elements. 




.. code:: python

    from enum import Enum 

    class TaskType(str, Enum):
    SERPAPI = "serpapi"
    CLICK = "click"
    GET_CURRENT_PAGE = "current_page"
    EXTRACT_HYPERLINKS = "extract_hyperlinks"
    EXTRACT_TEXT = "extract_text"
    GET_ELEMENTS = "get_elements"
    NAVIGATE_BACK = "navigate_back"
    NAVIGATE = "navigate"



|


Types
-----


This code defines a dictionary named TASK_TO_CLASS, which maps instances of the TaskType enumeration to 
corresponding classes that inherit from BaseTask. The purpose of this dictionary is to provide a convenient way to 
instantiate specific task classes based on their associated TaskType.




.. code:: python

    from typing import Dict, Type, Union

    from tasks.task_types import TaskType
    from tasks.task import BaseTask
    from tasks.serpapi import SerpAPI
    from tasks.playwright import *


    TASK_TO_CLASS: Dict[TaskType, Type[BaseTask]] = {
    TaskType.SERPAPI: SerpAPI,
    TaskType.CLICK: Click,
    TaskType.GET_CURRENT_PAGE: CurrentWebPage,
    TaskType.EXTRACT_HYPERLINKS: ExtractHyperlinks,
    TaskType.EXTRACT_TEXT: ExtractText,
    TaskType.GET_ELEMENTS: GetElements,
    TaskType.NAVIGATE_BACK: NavigateBack,
    TaskType.NAVIGATE: Navigate
    }



