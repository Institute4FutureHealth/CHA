from __future__ import annotations
from typing import Any, Dict, List, Union
from planners.planner import BasePlanner
from planners.action import Action, PlanFinish
from datapipes.datapipe import DataPipe
from response_generators.response_generator import BaseResponseGenerator
from tasks.initialize_task import initialize_task
from tasks.task import BaseTask
from planners.initialize_planner import initialize_planner
from datapipes.initialize_datapipe import initialize_datapipe
from response_generators.initialize_response_generator import initialize_response_generator
from pydantic import BaseModel
from CustomDebugFormatter import CustomDebugFormatter

from datapipes.datapipe_types import DatapipeType
from planners.planner_types import PlannerType
from response_generators.response_generator_types import ResponseGeneratorType
from tasks.task_types import TaskType
from llms.llm_types import LLMType
import logging
import re

class Orchestrator(BaseModel):
	"""
	**Description:**

		The Orchestrator class is the main execution heart of the CHA. All the components of the Orchestrator are initialized and executed here. \
		The Orchestrator will start a new answering cycle by calling the `run` method. From there, the planning is started, then tasks will be executed \
		one by one till the **Task Planner** decides that no more information is needed. Finally the **Task Planner** final answer \
		will be routed to the **Final Response Generator** to generate an empathic final response that is returned to the user.
	"""
	planner: BasePlanner = None
	datapipe: DataPipe = None
	promptist: Any = None
	response_generator: BaseResponseGenerator = None
	available_tasks: Dict[str, BaseTask] = {}
	max_retries: int = 16
	max_task_execute_retries: int = 3
	max_planner_execute_retries: int = 16
	max_final_answer_execute_retries: int = 3
	role: int = 0
	verbose: bool = False
	planner_logger: logging.Logger = None
	tasks_logger: logging.Logger = None
	orchestrator_logger: logging.Logger = None
	final_answer_generator_logger: logging.Logger = None
	promptist_logger: logging.Logger = None
	error_logger: logging.Logger = None

	class Config:
		"""Configuration for this pydantic object."""
		arbitrary_types_allowed = True

	def print_log(self, log_name: str, message: str):
		if self.verbose:
			if log_name == "planner":
				self.planner_logger.debug(message)
			if log_name == "task":
				self.tasks_logger.debug(message)
			if log_name == "orchestrator":
				self.orchestrator_logger.debug(message)
			if log_name == "response_generator":
				self.final_answer_generator_logger.debug(message)
			if log_name == "promptist":
				self.promptist_logger.debug(message)
			if log_name == "error":
				self.error_logger.debug(message)

	@classmethod
	def initialize(
		self,
		planner_llm: str = LLMType.OPENAI,
		planner_name: str = PlannerType.ZERO_SHOT_REACT_PLANNER,
		datapipe_name: str = DatapipeType.MEMORY,
		promptist_name: str = "",
		response_generator_llm: str = LLMType.OPENAI,
		response_generator_name: str = ResponseGeneratorType.BASE_GENERATOR,
		available_tasks: List[str] = [],
		verbose: bool = False,
		**kwargs
	) -> Orchestrator:
		"""
			This class method initializes the Orchestrator by setting up the planner, datapipe, promptist, response generator, and available tasks. 

		Args:
			planner_llm (str): LLMType to be used as LLM for planner.
			planner_name (str): PlannerType to be used as task planner.
			datapipe_name (str): DatapipeType to be used as data pipe.
			promptist_name (str): Not implemented yet!
			response_generator_llm (str): LLMType to be used as LLM for response generator.
			response_generator_name (str): ResponseGeneratorType to be used as response generator.
			available_tasks (List[str]): List of available task using TaskType.
			verbose (bool): Specifies if the debugging logs be printed or not.
			**kwargs (Any): Additional keyword arguments.
		Return:
			Orchestrator: Initialized Orchestrator instance.



		Example:
			.. code-block:: python

				from datapipes.datapipe_types import DatapipeType
				from planners.planner_types import PlannerType
				from response_generators.response_generator_types import ResponseGeneratorType
				from tasks.task_types import TaskType
				from llms.llm_types import LLMType
				from orchestrator.orchestrator import Orchestrator

				#If you want to use playwright task  
				from tasks.playwright.utils import create_sync_playwright_browser
				sync_browser = create_sync_playwright_browser()  
				#
				orchestrator = Orchestrator.initialize(      
					planner_llm=LLMType.OPENAI,
					planner_name=PlannerType.ZERO_SHOT_REACT_PLANNER, 
					datapipe_name=DatapipeType.MEMORY,
					promptist_name="",
					response_generator_llm=LLMType.OPENAI,
					response_generator_name=ResponseGeneratorType.BASE_GENERATOR,
					available_tasks=[TaskType.SERPAPI, TaskType.EXTRACT_TEXT], 
					sync_browser=sync_browser,
					verbose=self.verbose,
					**kwargs
				)

		"""

		if verbose:
			planner_logger = CustomDebugFormatter.create_logger('Planner', 'cyan')
			tasks_logger = CustomDebugFormatter.create_logger('Task', 'purple')
			orchestrator_logger = CustomDebugFormatter.create_logger('Orchestrator', 'green')
			final_answer_generator_logger = CustomDebugFormatter.create_logger('Response Generator', 'blue')
			promptist_logger = CustomDebugFormatter.create_logger('Promptist', 'blue')
			error_logger = CustomDebugFormatter.create_logger('Error', 'red')

		datapipe = initialize_datapipe(datapipe=datapipe_name, **kwargs)
		if verbose:
			orchestrator_logger.debug(f"Datapipe {datapipe_name} is successfully initialized.\n")

		tasks = {}      
		for task in available_tasks:
			kwargs["datapipe"] = datapipe
			tasks[task] = initialize_task(task=task, **kwargs)
			if verbose:
				orchestrator_logger.debug(f"Task '{task}' is successfully initialized.")
		
		planner = initialize_planner(tasks=list(tasks.values()), llm=planner_llm, planner=planner_name, **kwargs)
		if verbose:
			orchestrator_logger.debug(f"Planner {planner_name} is successfully initialized.")
		
		response_generator = initialize_response_generator(response_generator=response_generator_name, llm=response_generator_llm, **kwargs)
		if verbose:
			orchestrator_logger.debug(f"Response Generator {response_generator_name} is successfully initialized.")

		return self(
			planner=planner,
			datapipe=datapipe,
			promptist=None,
			response_generator=response_generator,
			available_tasks=tasks,
			verbose=verbose,
			planner_logger=planner_logger,
			tasks_logger=tasks_logger,
			orchestrator_logger=orchestrator_logger,
			final_answer_generator_logger=final_answer_generator_logger,
			promptist_logger=promptist_logger,
			error_logger=error_logger
		)

	def process_meta(self) -> bool:
		"""
			This method processes the meta information and returns a boolean value. Currently, it always returns False.

		Return:
			bool: False

		"""
		return False 
  
	def execute_task(self, action) -> str: 
		"""
			Execute the specified task based on the planner's selected **Action**. This method executes a specific task based on the provided action. It takes an action as input and retrieves the corresponding task from the available tasks dictionary. 
			It then executes the task with the given task input. If the task has an output_type, it stores the result in the datapipe and returns a message indicating the storage key. Otherwise, it returns the result directly.

		Args:
			action (Action): Action to be executed.
		Return:
			str: Result of the task execution.
			bool: If the task result should be directly returned to the user and stop planning.			
		"""  
		retries = 0
		self.print_log("task", f"---------------\nExecuting task:\nTask Name: {action.task}\nTask Inputs: {action.task_input}\n")    
		task_input = action.task_input    
		error_message = ""
		while retries < self.max_task_execute_retries:
			try:
				task = self.available_tasks[action.task] 
				result = task.execute(task_input)        
				self.print_log("task", f"Task is executed successfully\nResult: {result}\n---------------\n")
				return result, task.return_direct
			except Exception as e:
				self.print_log("error", f"Error running task:\n{e}\n---------------\n")
				logging.exception(e)
				error_message = e
				retries += 1
		return f"Error executing task {action.task}: {error_message}", False

	def planner_generate_prompt(self, query) -> str:
		"""
			Generate a prompt from the query to make it more understandable for both planner and response generator. \
			Not implemented yet.

		Args:
			query (str): Input query.
		Return:
			str: Generated prompt.

		"""
		return query 
	
	def _retrieve_last_action_from_datapip(self, previous_actions):
		print("previous action check", previous_actions)
		if len(previous_actions) > 0:
			for i in range(len(previous_actions)-1, -1, -1):
				if previous_actions[i].task in [TaskType.READ_FROM_DATAPIPE]:
					return None
				match = re.search(r"\$(datapipe:[^\$]+)\$", previous_actions[i].task_response)
				print("previous action check", previous_actions[i], match)
				if match:
					action = Action(TaskType.READ_FROM_DATAPIPE, match.group(1), "", "")
					action.task_response, ـ = self.execute_task(action)
					return action
		return None
		

	def response_generator_generate_prompt(
		self, 
		final_response: str = "", 
		history:str = "", 
		meta: List[str] = [], 
		previous_actions: List[Action] = [], 
		use_history: bool = False
	) -> str:
		prompt = (
		"MetaData: {meta}\n\n"
		"History: \n{history}\n\n"
		"Plan: \n{plan}\n\n"
		)
		if use_history:
			prompt = prompt.replace("{history}", history)

		prompt = prompt.replace("{meta}", ", ".join(meta))\
			.replace("{plan}", "".join([f"{self.available_tasks[action.task].chat_name}: {action.task_response}\n" if action.task in self.available_tasks else "" for action in previous_actions])) # + f"\n{final_response}")
		return prompt

	def plan(self, query, history, meta, previous_actions, use_history) -> List[Union[Action, PlanFinish]]: 
		"""
            Plan actions based on the query, history, and previous actions using the selected planner type. This method generates a plan of actions based on the provided query, history, previous actions, and use_history flag. \
            It calls the plan method of the planner and returns a list of actions or plan finishes.

        Args:
            query (str): Input query.
            history (str): History information.
            meta (Any): meta information.
            previous_actions (List[Action]): List of previous actions.
            use_history (bool): Flag indicating whether to use history.
        Return:
            List[Union[Action, PlanFinish]]: List of planned actions.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """   
		return self.planner.plan(query, history, meta, previous_actions, use_history)

	def generate_final_answer(self, query, thinker) -> str:
		"""
			Generate the final answer using the response generator. \
			This method generates the final answer based on the provided query and thinker. It calls the generate method of the response generator and returns the generated answer.

		Args:
			query (str): Input query.
			thinker (str): Thinking component.
		Return:
			str: Final generated answer.

		"""

		retries = 0
		while retries < self.max_final_answer_execute_retries:
			try:
				return self.response_generator.generate(query=query, thinker=thinker)
			except Exception as e:
				print(e)
				retries += 1
		return "We currently have problem processing your question. Please try again after a while."

	def run(
		self,
		query: str = "",
		meta: List[str] = [],
		history: str = "",
		use_history: bool = False,
		**kwargs: Any
    ) -> str:
		"""
			This method runs the orchestrator by taking a query, meta information, history, and other optional keyword arguments as input. 
			It initializes variables for tracking the execution, generates a prompt based on the query, and sets up a loop for executing actions. 
			Within the loop, it plans actions, executes tasks, and updates the previous actions list. If a PlanFinish action is encountered, the loop breaks, and the final response is set. 
			If any errors occur during execution, the loop retries a limited number of times before setting a final error response. Finally, it generates the final response using the prompt and thinker, and returns the final response along with the previous actions.

		Args:
			query (str): Input query.
			meta (List[str]): Meta information.
			history (str): History information.
			use_history (bool): Flag indicating whether to use history.
			**kwargs (Any): Additional keyword arguments.
		Return:
			Tuple[str, List[Action]]:Final response and list of previous actions.


		"""
		i = 0
		previous_actions = []
		meta_infos = ""
		for meta_data in meta:
			key = self.datapipe.store(meta_data)
			meta_infos += (
				f"The file with the name ${meta_data.split('/')[-1]}$ is stored with the key $datapipe:{key}$."
				"Pass this key to the tools when you want to send them over to the tool\n"
			)
		prompt = self.planner_generate_prompt(query)
		if "google_translate" in self.available_tasks:
			prompt = self.available_tasks["google_translate"].execute(prompt+"$#en")
			source_language = prompt[1]
			prompt = prompt[0]
		# history = self.available_tasks["google_translate"].execute(history+"$#en").text
		final_response = ""
		finished = False
		self.print_log("planner", f"Planing Started...\n")
		while True:
			try:
				self.print_log(
					"planner", f"Continueing Planing... Try number {i}\n\n")
				actions = self.plan(query=prompt, history=history, meta=meta_infos, previous_actions=previous_actions, use_history=use_history)
				for action in actions:
					if isinstance(action, PlanFinish):
						final_response = action.response
						finished = True
						break
					else:
						return_direct = False, False
						if not "Exception" in action.task:
							action.task_response, return_direct = self.execute_task(action)
							i = 0
						previous_actions.append(action)
						if return_direct:
							print("inside return direct")
							final_response = action.task_response
							finished = True
				if finished:
					action = self._retrieve_last_action_from_datapip(previous_actions)
					if action is not None:
						previous_actions.append(action)
					break
			except ValueError as error:
				self.print_log("error", f"Planing Error:\n{error}\n\n")
				i += 1
				if i > self.max_retries:
					final_response = "Problem preparing the answer. Please try again."
					break
				previous_actions.append(
					Action("Exception", "Invalid or incomplete response", "".join(error.args), ""))
		self.print_log("planner", f"Planner final response: {final_response}\nPlaning Ended...\n\n")

		final_response = self.response_generator_generate_prompt(final_response=final_response, history=history, meta=meta_infos, previous_actions=previous_actions, use_history=use_history)

		self.print_log("response_generator", f"Final Answer Generation Started...\n\nInput Prompt: \n{final_response}")
		final_response = self.generate_final_answer(query=query, thinker=final_response)
		self.print_log("response_generator", f"Response: {final_response}\n\nFinal Answer Generation Ended.\n")

		if "google_translate" in self.available_tasks:
			final_response = self.available_tasks["google_translate"].execute(
				f"{final_response}$#{source_language}")[0]
			
		return final_response, previous_actions
