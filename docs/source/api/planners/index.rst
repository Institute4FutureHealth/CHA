Planners
========



The **Task Planner** is the LLM-enabled decision-making core of the Orcestrator. Its primary responsibility is to generate a procedure to extract the required information for a response.
To achieve this, it interprets the user's query and accompanying metadata, identifying the necessary steps for execution.
Let's consider an example for clarification. The user inquires about her sleep quality, whether it can be improved, and if any action is necessary.
The Task Planner selects the appropriate procedure to provide an answer, drawing from available external sources.
It first examines the metadata if it includes last night's sleep data. Next, it requests analytical procedures (e.g., in AI Platforms) to extract sleep parameters, including sleep duration and wakefulness after sleep onset.
Once the required information is obtained, it then requests the retrieval of the most relevant information from online resources to provide an interpretation of sleep quality based on the obtained parameters.
For detailed information you can see our framework paper: `Paper <https://arxiv.org/abs/2310.02374>`_






.. toctree::
    :maxdepth: 1

    planners
    action
    initialize_planner
    types
    react/index
