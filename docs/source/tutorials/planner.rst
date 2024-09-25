.. _planner:

Planner Tree of Though Implementation
=====================================

In this tutorial, we elaborate on the implementation of the Tree of Thought prompting technique. We will describe how available tasks are introduced to the Tree of Thought, the process of curating and generating the planning prompt, and ultimately, how the final planning results are transformed into executable tasks by the Task Executor.

Task Planner and Planning Techniques
------------------------------------

The core component of the Task Planner is the selection of an appropriate planning technique. Among various techniques using large language models (LLMs) that have proven practical, we opted for the Tree of Thought approach.

Implementation Phases
---------------------

To effectively implement the Tree of Thought, we structured the planning process into two main sections:

1. **Preparation of the Planning Prompt**:
   Initially, we prepare a comprehensive prompt that includes a list of available tasks, relevant metadata, records of previously performed tasks, conversation history, and user input. This setup ensures the planner is thoroughly informed about the tasks it can call upon, the metadata that should be used or passed along, and the context of past interactions to prevent redundant planning and maintain the continuity of conversations.

   .. figure:: ../../figs/planner_prompt1.png
      :align: center
      :width: 100%
      :alt: The first stage Tree of Thought planning prompt

      The first stage Tree of Thought planning prompt. This phase utilizes the gathered information and the user's query to devise three distinct task sequences or strategies.

2. **Execution of the Chosen Strategy**:
   In the second stage of the planning process, our objective is to translate the chosen decision into sequences of task functions that the Orchestrator can understand and execute. Within the Orchestrator, we have implemented a function named `execute_task`, which serves as an interface to retrieve and execute tasks with the appropriate inputs accurately.

   .. figure:: ../../figs/planner_prompt2.png
      :align: center
      :width: 100%
      :alt: The second stage Tree of Thought planning prompt

      The second stage Tree of Thought planning prompt instructs the LLM to invoke the `execute_task` function, ensuring that the correct inputs are provided for each task.

Each strategy is designed to collect the necessary information to address the query efficiently. It is then asked to provide the pros and cons of each strategy, ultimately selecting the most suitable one as the final decision.
