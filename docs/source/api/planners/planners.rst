Planners
========




This code defines a base class called "BasePlanner" that inherits from the "BaseModel" class of the pydantic library. 
The BasePlanner class serves as a base for implementing specific planners.




- ``get_available_tasks`` : This method returns a string representation of the available tasks in the planner. It iterates over the available tasks and returns a formatted string for each task.

    .. autofunction:: planners.planner.BasePlanner.get_available_tasks
        :no-index:


|



- ``get_available_tasks_list`` : This method returns a list of the available task names in the planner. It iterates over the available tasks and returns a list containing the name of each task.

    .. autofunction:: planners.planner.BasePlanner.get_available_tasks_list
        :no-index:


|



- ``plan`` : This abstract method should be implemented in the derived classes. It takes a query, history, previous actions, and optional keyword arguments as input and returns a list of actions or plan finishes. 
  The specific implementation of the planner logic should be defined in this method.

    .. autofunction:: planners.planner.BasePlanner.plan
        :no-index:


|



- ``parse`` : This abstract method should also be implemented in the derived classes. It takes a query and optional keyword arguments as input and returns a list of actions. 
  The specific implementation of parsing logic for the planner should be defined in this method.

    .. autofunction:: planners.planner.BasePlanner.parse
        :no-index:





