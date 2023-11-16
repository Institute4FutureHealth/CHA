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


class Orchestrator(BaseModel):
    planner: BasePlanner = None
    datapipe: DataPipe = None
    promptist: Any = None
    response_generator: BaseResponseGenerator = None
    available_tasks: Dict[str, BaseTask] = {}
    max_retries: int = 16
    max_task_execute_retries: int = 3
    max_planner_execute_retries: int = 3
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
        Initialize the Orchestrator with selected components and available tasks.

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
            error_logger = CustomDebugFormatter.create_logger('Promptist', 'red')

        tasks = {}
        for task in available_tasks:
            tasks[task] = initialize_task(task=task, **kwargs)
            if verbose:
                orchestrator_logger.debug(f"Task '{task}' is successfully initialized.")

        planner = initialize_planner(tasks=list(tasks.values()), llm=planner_llm, planner=planner_name, **kwargs)
        if verbose:
            orchestrator_logger.debug(f"Planner {planner_name} is successfully initialized.")

        response_generator = initialize_response_generator(response_generator=response_generator_name,
                                                           llm=response_generator_llm, **kwargs)
        if verbose:
            orchestrator_logger.debug(f"Response Generator {response_generator_name} is successfully initialized.")

        datapipe = initialize_datapipe(datapipe=datapipe_name, **kwargs)
        if verbose:
            orchestrator_logger.debug(f"Datapipe {datapipe_name} is successfully initialized.\n")

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
        Placeholder method returning False.

        Return:
            bool: False



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        return False

    def execute_task(self, action: Action) -> str:
        """
        Execute the specified task based on the planner selected **Action**.

        Args:
            action (Action): Action to be executed.
        Return:
            str: Result of the task execution.

        """

        retries = 0
        self.print_log("task",
                       f"---------------\nExecuting task:\nTask Name: {action.task}\nTask Inputs: {action.task_input}\n")
        task_input = action.task_input
        if "datapipe" in task_input:
            self.print_log("task", "Tasks data is retrieved from the DataPipe\n")
            task_input = self.datapipe.retrieve(action.task_input.split(":")[-1])

        while retries < self.max_task_execute_retries:
            try:
                task = self.available_tasks[action.task]
                result = task.execute(task_input)
                if task.output_type:
                    key = self.datapipe.store(result)
                    self.print_log("task", f"Task result is stored in the DataPipe\n\n")
                    return (
                        f"The result of the tool ${task.name}$ is stored in the datapipe with key: $datapipe:{key}$"
                        "pass this key to other tools to get access to the result."
                    )
                self.print_log("task", f"Task is executed successfully\nResult: {result}\n---------------\n")
                return result, task.return_direct
            except Exception as e:
                self.print_log("error", f"Error running task:\n{e}\n---------------\n")
                retries += 1
        return f"Error executing task {action.task}", False

    def generate_prompt(self, query) -> str:
        """
        Generate a prompt for the orchestrator.

        Args:
            query (str): Input query.
        Return:
            str: Generated prompt.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        return query

    def plan(self, query, history, meta, previous_actions, use_history) -> List[Union[Action, PlanFinish]]:
        """
        Plan actions based on the query, history, and previous actions using the planner.

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

        retries = 0
        while retries < self.max_planner_execute_retries:
            try:
                return self.planner.plan(query, history, meta, previous_actions, use_history)
            except Exception as e:
                print(e)
                retries += 1
        return [PlanFinish("Error planning, please try to ask your question again", "")]

    def generate_final_answer(self, query, thinker) -> str:
        """
        Generate the final answer using the response generator.

        Args:
            query (str): Input query.
            thinker (str): Thinking component.
        Return:
            str: Final generated answer.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

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
        Run the orchestrator to process a query.

        Args:
            query (str): Input query.
            meta (List[str]): Meta information.
            history (str): History information.
            use_history (bool): Flag indicating whether to use history.
            **kwargs (Any): Additional keyword arguments.
        Return:
            Tuple[str, List[Action]]:Final response and list of previous actions.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

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
        prompt = self.generate_prompt(query)
        if "google_translate" in self.available_tasks:
            prompt = self.available_tasks["google_translate"].execute(prompt + "$#en")
            source_language = prompt[1]
            prompt = prompt[0]
        # history = self.available_tasks["google_translate"].execute(history+"$#en").text
        final_response = ""
        finished = False
        while True:
            try:
                self.print_log("planner", f"Planing Started... Try number {i}\n\n")
                actions = self.plan(query=prompt, history=history, meta=meta_infos, previous_actions=previous_actions,
                                    use_history=use_history)
                for action in actions:
                    if isinstance(action, PlanFinish):
                        final_response = action.response
                        finished = True
                        break
                    else:
                        action.task_response, return_direct = self.execute_task(action)
                        previous_actions.append(action)
                        if return_direct:
                            final_response = action.task_response
                            finished = True
                        i = 0
                if finished:
                    break
            except ValueError as error:
                self.print_log("error", "Planing Error:\n{error}\n\n")
                i += 1
                if i > self.max_retries:
                    final_response = "Problem preparing the answer. Please try again."
                    break
                previous_actions.append(Action("Exception", "Invalid or incomplete response", "".join(error.args), ""))
        self.print_log("planner", f"Planner final response: {final_response}\nPlaning Ended...\n\n")

        final_response = self.generate_prompt(final_response)

        self.print_log("response_generator", "Final Answer Generation Started...\n")
        final_response = self.generate_final_answer(query=query, thinker=final_response)
        self.print_log("response_generator", f"Response: {final_response}\n\nFinal Answer Generation Ended.\n")

        if "google_translate" in self.available_tasks:
            final_response = self.available_tasks["google_translate"].execute(f"{final_response}$#{source_language}")[0]
        return final_response, previous_actions
