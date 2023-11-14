Initialize planner
==================





This code defines a function called initialize_planner which is used to initialize a planner object based on the specified input.



- ``initialize_planner`` : The function first checks if the specified planner type (planner) and LLM type (llm) are valid by comparing them to the predefined dictionaries PLANNER_TO_CLASS and LLM_TO_CLASS respectively. 
  If either of the types is not found in the dictionaries, a ValueError is raised.

    .. py:function:: initialize_planner(tasks: List[BaseTask], llm: str="openai", planner: str = "zero-shot-react-planner", **kwargs: Any)

        Initialize a planner with specified tasks, language model, and planner type.

        :param tasks: List of tasks to be associated with the planner.
        :type tasks: List[BaseTask]
        :param llm: Language model type.
        :type llm: str
        :param planner: Planner type.
        :type planner: str
        :param **kwargs: Additional keyword arguments.
        :type **kwargs: Any
        :return: Initialized planner instance.
        :rtype: BasePlanner
        :rise ValueError: If the specified planner or language model type is not recognized.









