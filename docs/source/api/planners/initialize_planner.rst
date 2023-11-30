Initialize planner
==================

This code defines a function called initialize_planner which is used to initialize a planner object based on the specified input.


- ``initialize_planner`` : The function first checks if the specified planner type (planner) and LLM type (llm) are valid by comparing them to the predefined dictionaries PLANNER_TO_CLASS and LLM_TO_CLASS respectively.
  If either of the types is not found in the dictionaries, a ValueError is raised.

    .. autofunction:: planners.initialize_planner.initialize_planner
      :no-index:
