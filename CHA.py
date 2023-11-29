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
    planner: str = PlannerType.ZERO_SHOT_REACT_PLANNER
    datapipe: str = DatapipeType.MEMORY
    promptist: str = ""
    response_generator_llm: str = LLMType.OPENAI
    response_generator: str = ResponseGeneratorType.BASE_GENERATOR
    meta: List[str] = []
    verbose: bool = False

    def _generate_history(
        self, chat_history: List[Tuple[str, str]] = None
    ) -> str:
        if chat_history is None:
            chat_history = []
        print("chat history", chat_history)
        history = "".join(
            [
                f"\n------------\nUser: {chat[0]}\nCHA: {chat[1]}\n------------\n"
                for chat in chat_history
            ]
        )
        if len(self.previous_actions) > 0:
            history += "Previous Actions: " + "".join(
                [
                    f"\n------------\naction: {action.task}\naction_response: {action.task_response}\n------------\n"
                    for action in self.previous_actions
                    if action.task != "Exception"
                ]
            )
        return history

    def _run(
        self,
        query: str,
        chat_history: List[Tuple[str, str]] = None,
        tasks_list: List[str] = None,
        use_history: bool = False,
        **kwargs,
    ) -> str:
        if chat_history is None:
            chat_history = []
        if tasks_list is None:
            tasks_list = []

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
                verbose=self.verbose,
                **kwargs,
            )

        response, actions = self.orchestrator.run(
            query=query,
            history=history,
            meta=self.meta,
            use_history=use_history,
        )
        self.previous_actions += actions

        return response

    def respond(self, message, chat_history, check_box, tasks_list):
        response = self._run(
            query=message,
            chat_history=chat_history,
            tasks_list=tasks_list,
            use_history=check_box,
        )
        chat_history.append((message, response))
        return "", chat_history

    def reset(self):
        self.previous_actions = []

    def run_with_interface(self):
        available_tasks = [key.value for key in TASK_TO_CLASS.keys()]
        interface = Interface()
        interface.prepare_interface(
            respond=self.respond,
            reset=self.reset,
            upload_meta=self.upload_meta,
            available_tasks=available_tasks,
        )

    def upload_meta(self, history, file):
        history = history + [((file.name,), None)]
        self.meta.append(file.name)
        return history

    def run(
        self,
        query: str,
        chat_history: List[Tuple[str, str]] = None,
        available_tasks: List[str] = None,
        use_history: bool = False,
    ) -> str:
        if chat_history is None:
            chat_history = []
        if available_tasks is None:
            available_tasks = []

        return self._run(
            query=query,
            chat_history=chat_history,
            tasks_list=available_tasks,
            use_history=use_history,
        )
