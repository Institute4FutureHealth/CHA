Planners
========




This code defines a base class called "BasePlanner" that inherits from the "BaseModel" class of the pydantic library. 
The BasePlanner class serves as a base for implementing specific planners.




- ``get_available_tasks`` : This method returns a string representation of the available tasks in the planner. It iterates over the available tasks and returns a formatted string for each task.

    .. py:function:: get_available_tasks(self)

        Get a formatted string representation of available tasks.

        :return: Formatted string of available tasks.
        :rtype: str


|



- ``get_available_tasks_list`` : This method returns a list of the available task names in the planner. It iterates over the available tasks and returns a list containing the name of each task.

    .. py:function:: get_available_tasks_list(self)

        Get a list of names of available tasks.

        :return: List of task names.
        :rtype: List[str]


|



- ``plan`` : This abstract method should be implemented in the derived classes. It takes a query, history, previous actions, and optional keyword arguments as input and returns a list of actions or plan finishes. 
  The specific implementation of the planner logic should be defined in this method.

    .. py:function:: plan(self, query: str, history: str, previous_actions: List[Action], use_history: bool = False, **kwargs: Any)

        Abstract method for generating a plan based on the input query and history.

        :param query: Input query.
        :type query: str
        :param history: History information.
        :type history: str
        :param previous_actions: List of previous actions.
        :type previous_actions: List[Action]
        :param use_history: Flag indicating whether to use history.
        :type use_history: bool
        :param **kwargs: Additional keyword arguments.
        :type **kwargs: Any
        :return: List of planned actions or finishing signals.
        :rtype: List[Union[Action, PlanFinish]]


|



- ``parse`` : This abstract method should also be implemented in the derived classes. It takes a query and optional keyword arguments as input and returns a list of actions. 
  The specific implementation of parsing logic for the planner should be defined in this method.

    .. py:function:: parse(self, query: str, **kwargs: Any,)

        Abstract method for parsing the input query into actions.

        :param query (str): Input query.
        :type query: str
        :param **kwargs: Additional keyword arguments.
        :type **kwargs: Any
        :return: List of parsed actions.
        :rtype: List[Action]





