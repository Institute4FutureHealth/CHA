from __future__ import annotations

import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel

from CustomDebugFormatter import CustomDebugFormatter
from datapipes.datapipe import DataPipe
from datapipes.datapipe_types import DatapipeType
from datapipes.initialize_datapipe import initialize_datapipe
from llms.llm_types import LLMType
from orchestrator.action import Action
from planners.action import PlanFinish
from planners.initialize_planner import initialize_planner
from planners.planner import BasePlanner
from planners.planner_types import PlannerType
from response_generators.initialize_response_generator import (
    initialize_response_generator,
)
from response_generators.response_generator import (
    BaseResponseGenerator,
)
from response_generators.response_generator_types import (
    ResponseGeneratorType,
)
from tasks.initialize_task import initialize_task
from tasks.task import BaseTask
from tasks.task_types import TaskType


class Orchestrator(BaseModel):
    """
    **Description:**

        The Orchestrator class is the main execution heart of the CHA. All the components of the Orchestrator are initialized and executed here.
        The Orchestrator will start a new answering cycle by calling the `run` method. From there, the planning is started,
        then tasks will be executed one by one till the **Task Planner** decides that no more information is needed.
        Finally the **Task Planner** final answer will be routed to the **Final Response Generator** to generate an empathic final
        response that is returned to the user.
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
    planner_logger: Optional[logging.Logger] = None
    tasks_logger: Optional[logging.Logger] = None
    orchestrator_logger: Optional[logging.Logger] = None
    final_answer_generator_logger: Optional[logging.Logger] = None
    promptist_logger: Optional[logging.Logger] = None
    error_logger: Optional[logging.Logger] = None
    previous_actions: List[str] = []
    current_actions: List[str] = []
    runtime: Dict[str, bool] = {}

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
        available_tasks: Optional[List[str]] = None,
        previous_actions: List[Action] = None,
        verbose: bool = False,
        **kwargs,
    ) -> Orchestrator:
        """
            This class method initializes the Orchestrator by setting up the planner, datapipe, promptist, response generator,
            and available tasks.

        Args:
            planner_llm (str): LLMType to be used as LLM for planner.
            planner_name (str): PlannerType to be used as task planner.
            datapipe_name (str): DatapipeType to be used as data pipe.
            promptist_name (str): Not implemented yet!
            response_generator_llm (str): LLMType to be used as LLM for response generator.
            response_generator_name (str): ResponseGeneratorType to be used as response generator.
            available_tasks (List[str]): List of available task using TaskType.
            previous_actions (List[Action]): List of previous actions.
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
        if available_tasks is None:
            available_tasks = []
        if previous_actions is None:
            previous_actions = []

        planner_logger = (
            tasks_logger
        ) = (
            orchestrator_logger
        ) = (
            final_answer_generator_logger
        ) = promptist_logger = error_logger = None
        if verbose:
            planner_logger = CustomDebugFormatter.create_logger(
                "Planner", "cyan"
            )
            tasks_logger = CustomDebugFormatter.create_logger(
                "Task", "purple"
            )
            orchestrator_logger = CustomDebugFormatter.create_logger(
                "Orchestrator", "green"
            )
            final_answer_generator_logger = (
                CustomDebugFormatter.create_logger(
                    "Response Generator", "blue"
                )
            )
            promptist_logger = CustomDebugFormatter.create_logger(
                "Promptist", "blue"
            )
            error_logger = CustomDebugFormatter.create_logger(
                "Error", "red"
            )

        datapipe = initialize_datapipe(
            datapipe=datapipe_name, **kwargs
        )
        if verbose:
            orchestrator_logger.debug(
                f"Datapipe {datapipe_name} is successfully initialized.\n"
            )

        tasks = {}
        for task in available_tasks:
            kwargs["datapipe"] = datapipe
            tasks[task] = initialize_task(task=task, **kwargs)
            if verbose:
                orchestrator_logger.debug(
                    f"Task '{task}' is successfully initialized."
                )

        planner = initialize_planner(
            tasks=list(tasks.values()),
            llm=planner_llm,
            planner=planner_name,
            **kwargs,
        )
        if verbose:
            orchestrator_logger.debug(
                f"Planner {planner_name} is successfully initialized."
            )

        response_generator = initialize_response_generator(
            response_generator=response_generator_name,
            llm=response_generator_llm,
            **kwargs,
        )
        if verbose:
            orchestrator_logger.debug(
                f"Response Generator {response_generator_name} is successfully initialized."
            )

        return self(
            planner=planner,
            datapipe=datapipe,
            promptist=None,
            response_generator=response_generator,
            available_tasks=tasks,
            verbose=verbose,
            previous_actions=previous_actions,
            current_actions=[],
            planner_logger=planner_logger,
            tasks_logger=tasks_logger,
            orchestrator_logger=orchestrator_logger,
            final_answer_generator_logger=final_answer_generator_logger,
            promptist_logger=promptist_logger,
            error_logger=error_logger,
        )

    def process_meta(self) -> bool:
        """
            This method processes the meta information and returns a boolean value. Currently, it always returns False.

        Return:
            bool: False

        """
        return False

    def _update_runtime(self, action: Action = None):
        if action.output_type:
            self.runtime[action.task_response] = False
        for task_input in action.task_inputs:
            if task_input in self.runtime:
                self.runtime[task_input] = True

    def execute_task(
        self, task_name: str, task_inputs: List[str]
    ) -> Any:
        """
            Execute the specified task based on the planner's selected **Action**. This method executes a specific task based on the provided action.
            It takes an action as input and retrieves the corresponding task from the available tasks dictionary.
            It then executes the task with the given task input. If the task has an output_type, it stores the result in the datapipe and returns
            a message indicating the storage key. Otherwise, it returns the result directly.

        Args:
            task_name (str): The name of the Task.
            task_inputs List(str): The list of the inputs for the task.
        Return:
            str: Result of the task execution.
            bool: If the task result should be directly returned to the user and stop planning.
        """
        self.print_log(
            "task",
            f"---------------\nExecuting task:\nTask Name: {task_name}\nTask Inputs: {task_inputs}\n",
        )
        error_message = ""

        try:
            task = self.available_tasks[task_name]
            result = task.execute(task_inputs)
            self.print_log(
                "task",
                f"Task is executed successfully\nResult: {result}\n---------------\n",
            )
            action = Action(
                task_name=task_name,
                task_inputs=task_inputs,
                task_response=result,
                output_type=task.output_type,
                datapipe=self.datapipe,
            )

            self._update_runtime(action)

            self.previous_actions.append(action)
            self.current_actions.append(action)
            return result  # , task.return_direct
        except Exception as e:
            self.print_log(
                "error",
                f"Error running task: \n{e}\n---------------\n",
            )
            logging.exception(e)
            error_message = e
            raise ValueError(
                f"Error executing task {task_name}: {error_message}\n\nTry again with different inputs."
            )

    def planner_generate_prompt(self, query) -> str:
        """
            Generate a prompt from the query to make it more understandable for both planner and response generator.
            Not implemented yet.

        Args:
                query (str): Input query.
        Return:
                str: Generated prompt.

        """
        return query

    def _prepare_planner_response_for_response_generator(self):
        print("runtime", self.runtime)
        final_response = ""
        for action in self.current_actions:
            final_response += action.dict(
                (
                    action.output_type
                    and not self.runtime[action.task_response]
                )
            )
        return final_response

    def response_generator_generate_prompt(
        self,
        final_response: str = "",
        history: str = "",
        meta: List[str] = None,
        use_history: bool = False,
    ) -> str:
        if meta is None:
            meta = []

        prompt = "MetaData: {meta}\n\nHistory: \n{history}\n\n"
        if use_history:
            prompt = prompt.replace("{history}", history)

        prompt = (
            prompt.replace("{meta}", ", ".join(meta))
            + f"\n{final_response}"
        )
        return prompt

    def plan(self, query, history, meta, use_history) -> str:
        """
            Plan actions based on the query, history, and previous actions using the selected planner type.
            This method generates a plan of actions based on the provided query, history, previous actions, and use_history flag.
            It calls the plan method of the planner and returns a list of actions or plan finishes.

        Args:
            query (str): Input query.
            history (str): History information.
            meta (Any): meta information.
            use_history (bool): Flag indicating whether to use history.
        Return:
            str: A python code block will be returnd to be executed by Task Executor.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """
        return self.planner.plan(
            query, history, meta, self.previous_actions, use_history
        )

    def generate_final_answer(self, query, thinker) -> str:
        """
            Generate the final answer using the response generator.
            This method generates the final answer based on the provided query and thinker.
            It calls the generate method of the response generator and returns the generated answer.

        Args:
            query (str): Input query.
            thinker (str): Thinking component.
        Return:
            str: Final generated answer.

        """

        retries = 0
        while retries < self.max_final_answer_execute_retries:
            try:
                return self.response_generator.generate(
                    query=query, thinker=thinker
                )
            except Exception as e:
                print(e)
                retries += 1
        return "We currently have problem processing your question. Please try again after a while."

    def run(
        self,
        query: str,
        meta: List[str] = None,
        history: str = "",
        use_history: bool = False,
        **kwargs: Any,
    ) -> str:
        """
            This method runs the orchestrator by taking a query, meta information, history, and other optional keyword arguments as input.
            It initializes variables for tracking the execution, generates a prompt based on the query, and sets up a loop for executing actions.
            Within the loop, it plans actions, executes tasks, and updates the previous actions list.
            If a PlanFinish action is encountered, the loop breaks, and the final response is set.
            If any errors occur during execution, the loop retries a limited number of times before setting a final error response.
            Finally, it generates the final response using the prompt and thinker, and returns the final response along with the previous actions.

        Args:
            query (str): Input query.
            meta (List[str]): Meta information.
            history (str): History information.
            use_history (bool): Flag indicating whether to use history.
            **kwargs (Any): Additional keyword arguments.
        Return:
            str: The final response to shown to the user.


        """
        if meta is None:
            meta = []
        i = 0
        meta_infos = ""
        for meta_data in meta:
            key = self.datapipe.store(meta_data)
            meta_infos += (
                f"The file with the name ${meta_data.split('/')[-1]}$ is stored with the key $datapipe:{key}$."
                "Pass this key to the tools when you want to send them over to the tool\n"
            )
        prompt = self.planner_generate_prompt(query)
        if "google_translate" in self.available_tasks:
            prompt = self.available_tasks["google_translate"].execute(
                [prompt, "en"]
            )
            source_language = prompt[1]
            prompt = prompt[0]
        # history = self.available_tasks["google_translate"].execute(history+"$#en").text
        final_response = ""
        finished = False
        self.print_log("planner", "Planning Started...\n")
        while True:
            try:
                self.print_log(
                    "planner",
                    f"Continueing Planning... Try number {i}\n\n",
                )
                actions = self.plan(
                    query=prompt,
                    history=history,
                    meta=meta_infos,
                    use_history=use_history,
                )
                vars = {}
                exec(actions, locals(), vars)
                final_response = (
                    self._prepare_planner_response_for_response_generator()
                )
                print("final resp", final_response)
                self.current_actions = []
                self.runtime = {}
                break
            except (Exception, SystemExit) as error:
                self.print_log(
                    "error", f"Planning Error:\n{error}\n\n"
                )
                self.current_actions = []
                i += 1
                if i > self.max_retries:
                    final_response = "Problem preparing the answer. Please try again."
                    break

        self.print_log(
            "planner",
            f"Planner final response: {final_response}\nPlanning Ended...\n\n",
        )

        final_response = self.response_generator_generate_prompt(
            final_response=final_response,
            history=history,
            meta=meta_infos,
            use_history=use_history,
        )

        self.print_log(
            "response_generator",
            f"Final Answer Generation Started...\nInput Prompt: \n\n{final_response}",
        )
        final_response = self.generate_final_answer(
            query=query, thinker=final_response
        )
        self.print_log(
            "response_generator",
            f"Response: {final_response}\n\nFinal Answer Generation Ended.\n",
        )

        if "google_translate" in self.available_tasks:
            final_response = self.available_tasks[
                "google_translate"
            ].execute([final_response, source_language])[0]

        return final_response
