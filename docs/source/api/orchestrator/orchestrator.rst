Orchestrator
============





This code defines a class called "Orchestrator" that inherits from the "BaseModel" class of the pydantic library. 
The Orchestrator class represents an orchestrator that coordinates the execution of tasks based on input queries.




- ``initialize`` : This class method initializes the Orchestrator by setting up the planner, datapipe, promptist, response generator, and available tasks. 
  It takes several parameters such as the names of the planner, datapipe, promptist, response generator, and a list of available tasks. It initializes the tasks, planner, response generator, and datapipe using their corresponding initialization methods. 
  Finally, it returns an instance of the Orchestrator class.

    .. py:function:: initialize(self, planner_llm: str = "openai", planner: str = "zero-shot-react-planner", datapipe: str = "memory", promptist: str = "", response_generator: str = "base-generator", response_generator_llm: str = "openai", available_tasks: List[str] = [], **kwargs)

        Initialize the Orchestrator with specified components and tasks.

        :param planner_llm: Language model for the planner.
        :type planner_llm: str
        :param planner: Name of the planner.
        :type planner: str
        :param datapipe: Name of the data pipe.
        :type datapipe: str
        :param promptist: Name of the promptist.
        :type promptist: str
        :param response_generator: Name of the response generator.
        :type response_generator: str
        :param response_generator_llm: Language model for the response generator.
        :type response_generator_llm: str
        :param available_tasks: List of available task names.
        :type available_tasks: List[str]
        :param **kwargs: Additional keyword arguments.
        :type **kwargs: Any
        :return: Initialized Orchestrator instance.
        :rtype: Orchestrator


|



- ``process_meta`` : This method processes the meta information and returns a boolean value. Currently, it always returns False.

    .. py:function:: process_meta(self)

        Placeholder method returning False.

        :return: False
        :rtype: bool


|



- ``execute_task`` : This method executes a specific task based on the provided action. It takes an action as input and retrieves the corresponding task from the available tasks dictionary. 
  It then executes the task with the given task input. If the task has an output_type, it stores the result in the datapipe and returns a message indicating the storage key. Otherwise, it returns the result directly.

    .. py:function:: execute_task(self, action)

        Execute the specified task and store the result in the datapipe.

        :param action: Task action to be executed.
        :type action: object
        :return: Result of the task execution.
        :rtype: str


|



- ``generate_prompt`` : This method generates a prompt based on the provided query. It simply returns the query as the prompt.

    .. py:function:: generate_prompt(self, query)

        Generate a prompt for the orchestrator.

        :param query: Input query.
        :type query: str
        :return: Generated prompt.
        :rtype: str


|



- ``plan`` : This method generates a plan of actions based on the provided query, history, previous actions, and use_history flag. It calls the plan method of the planner and returns a list of actions or plan finishes.

    .. py:function:: plan(self, query, history, previous_actions, use_history)

        Plan actions based on the query, history, and previous actions using the planner.

        :param query: Input query.
        :type query: str
        :param history: History information.
        :type history: str
        :param previous_actions: List of previous actions.
        :type previous_actions: List[Action]
        :param use_history: Flag indicating whether to use history.
        :type use_history: bool
        :return: List of planned actions.
        :rtype: List[Union[Action, PlanFinish]]


|



- ``generate_final_answer`` : This method generates the final answer based on the provided query and thinker. It calls the generate method of the response generator and returns the generated answer.

    .. py:function:: generate_final_answer(self, query, thinker)

        Generate the final answer using the response generator.

        :param query: Input query.
        :type query: str
        :param thinker: Thinking component.
        :type thinker: str
        :return: Final generated answer.
        :rtype: str


|



- ``run`` : This method runs the orchestrator by taking a query, meta information, history, and other optional keyword arguments as input. 
  It initializes variables for tracking the execution, generates a prompt based on the query, and sets up a loop for executing actions. 
  Within the loop, it plans actions, executes tasks, and updates the previous actions list. If a PlanFinish action is encountered, the loop breaks, and the final response is set. 
  If any errors occur during execution, the loop retries a limited number of times before setting a final error response. Finally, it generates the final response using the prompt and thinker, and returns the final response along with the previous actions.

    .. py:function:: run(self, query: str = "", meta: Any = {}, history: str = "", use_history: bool = False, **kwargs: Any)

        Run the orchestrator to process a query.

        :param query: Input query.
        :type query: str
        :param meta: Meta information.
        :type meta: Any
        :param history: History information.
        :type history: str
        :param use_history: Flag indicating whether to use history.
        :type use_history: bool
        :param **kwargs: Additional keyword arguments.
        :type **kwargs: Any
        :return: Final response and list of previous actions.
        :rtype: Tuple[str, List[Action]]






