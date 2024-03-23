from typing import Any
from typing import List
from typing import Tuple

from pydantic import BaseModel

from datapipes.datapipe_types import DatapipeType
from interface.base import Interface
from llms.llm_types import LLMType
from orchestrator.orchestrator import Orchestrator
from planners.action import Action
from planners.planner_types import PlannerType
from response_generators.response_generator_types import (
    ResponseGeneratorType,
)
from tasks.playwright.utils import create_sync_playwright_browser
from tasks.task_types import TaskType
from tasks.types import TASK_TO_CLASS


class CHA(BaseModel):
    name: str = "CHA"
    previous_actions: List[Action] = []
    orchestrator: Orchestrator = None
    sync_browser: Any = None
    planner_llm: str = LLMType.OPENAI
    planner: str = PlannerType.TREE_OF_THOUGHT
    datapipe: str = DatapipeType.MEMORY
    promptist: str = ""
    response_generator_llm: str = LLMType.OPENAI
    response_generator: str = ResponseGeneratorType.BASE_GENERATOR
    verbose: bool = False

    def _generate_history(
        self, chat_history: List[Tuple[str, str]] = None
    ) -> str:
        if chat_history is None:
            chat_history = []

        history = "".join(
            [
                f"\n------------\nUser: {chat[0]}\nCHA: {chat[1]}\n------------\n"
                for chat in chat_history
            ]
        )
        return history

    def _run(
        self,
        query: str,
        meta: List[str] = None,
        chat_history: List[Tuple[str, str]] = None,
        tasks_list: List[str] = None,
        use_history: bool = False,
        **kwargs,
    ) -> str:
        if chat_history is None:
            chat_history = []
        if tasks_list is None:
            tasks_list = []
        if meta is None:
            meta = []

        history = self._generate_history(chat_history=chat_history)
        # query += f"User: {message}"
        # print(orchestrator.run("what is the name of the girlfriend of Leonardo Dicaperio?"))
        if self.sync_browser is None:
            self.sync_browser = create_sync_playwright_browser()

        if self.orchestrator is None:
            self.orchestrator = Orchestrator.initialize(
                planner_llm=self.planner_llm,
                planner_name=self.planner,
                datapipe_name=self.datapipe,
                promptist_name=self.promptist,
                response_generator_llm=self.response_generator_llm,
                response_generator_name=self.response_generator,
                available_tasks=tasks_list,
                sync_browser=self.sync_browser,
                previous_actions=self.previous_actions,
                verbose=self.verbose,
                **kwargs,
            )

        response = self.orchestrator.run(
            query=query,
            meta=meta,
            history=history,
            use_history=use_history,
            **kwargs,
        )

        return response

    def reset(self):
        self.previous_actions = []

    def run_with_interface(self):
        available_tasks = [key.value for key in TASK_TO_CLASS.keys()]
        interface = Interface(run_query=self.run)
        interface.prepare_interface(
            reset=self.reset,
            available_tasks=available_tasks,
        )

    def run(
        self,
        query: str,
        meta: List[str] = None,
        chat_history: List[Tuple[str, str]] = None,
        available_tasks: List[str] = None,
        use_history: bool = False,
        **kwargs,
    ) -> str:
        if chat_history is None:
            chat_history = []
        if available_tasks is None:
            available_tasks = []
        if meta is None:
            meta = []

        return self._run(
            query=query,
            meta=meta,
            chat_history=chat_history,
            tasks_list=available_tasks,
            use_history=use_history,
            **kwargs,
        )
