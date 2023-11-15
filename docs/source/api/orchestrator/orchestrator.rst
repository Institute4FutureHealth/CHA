Orchestrator
============





This code defines a class called "Orchestrator" that inherits from the "BaseModel" class of the pydantic library. 
The Orchestrator class represents an orchestrator that coordinates the execution of tasks based on input queries.




- ``initialize`` : This class method initializes the Orchestrator by setting up the planner, datapipe, promptist, response generator, and available tasks. 
  It takes several parameters such as the names of the planner, datapipe, promptist, response generator, and a list of available tasks. It initializes the tasks, planner, response generator, and datapipe using their corresponding initialization methods. 
  Finally, it returns an instance of the Orchestrator class.

    .. autofunction:: orchestrator.orchestrator.Orchestrator.initialize
        :no-index:


|



- ``process_meta`` : This method processes the meta information and returns a boolean value. Currently, it always returns False.

    .. autofunction:: orchestrator.orchestrator.Orchestrator.process_meta
        :no-index:


|



- ``execute_task`` : This method executes a specific task based on the provided action. It takes an action as input and retrieves the corresponding task from the available tasks dictionary. 
  It then executes the task with the given task input. If the task has an output_type, it stores the result in the datapipe and returns a message indicating the storage key. Otherwise, it returns the result directly.

    .. autofunction:: orchestrator.orchestrator.Orchestrator.execute_task
        :no-index:


|



- ``generate_prompt`` : This method generates a prompt based on the provided query. It simply returns the query as the prompt.

    .. autofunction:: orchestrator.orchestrator.Orchestrator.generate_prompt
        :no-index:


|



- ``plan`` : This method generates a plan of actions based on the provided query, history, previous actions, and use_history flag. It calls the plan method of the planner and returns a list of actions or plan finishes.

    .. autofunction:: orchestrator.orchestrator.Orchestrator.plan
        :no-index:


|



- ``generate_final_answer`` : This method generates the final answer based on the provided query and thinker. It calls the generate method of the response generator and returns the generated answer.

    .. autofunction:: orchestrator.orchestrator.Orchestrator.generate_final_answer
        :no-index:


|



- ``run`` : This method runs the orchestrator by taking a query, meta information, history, and other optional keyword arguments as input. 
  It initializes variables for tracking the execution, generates a prompt based on the query, and sets up a loop for executing actions. 
  Within the loop, it plans actions, executes tasks, and updates the previous actions list. If a PlanFinish action is encountered, the loop breaks, and the final response is set. 
  If any errors occur during execution, the loop retries a limited number of times before setting a final error response. Finally, it generates the final response using the prompt and thinker, and returns the final response along with the previous actions.

    .. autofunction:: orchestrator.orchestrator.Orchestrator.run
        :no-index:






