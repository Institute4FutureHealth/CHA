from planners.action import Action
from typing import List, Any, Tuple, Dict
from orchestrator.orchestrator import Orchestrator
from interface.base import Interface
from tasks.types import TASK_TO_CLASS
from tasks.playwright.utils import create_sync_playwright_browser
from pydantic import BaseModel

from datapipes.datapipe_types import DatapipeType
from planners.planner_types import PlannerType
from response_generators.response_generator_types import ResponseGeneratorType
from tasks.task_types import TaskType
from llms.llm_types import LLMType

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
                  self, 
                  chat_history: List[Tuple[str, str]] = []
                ) -> str:
    print("chat history", chat_history)
    history = "".join([f"User: {chat[0]}\nCHA: {chat[1]}\n" for chat in chat_history])
    if len(self.previous_actions) > 0:
      history += "Previous Actions: " + "\n\n".join([f"action: {action.task}\naction_response: {action.task_response}" for action in self.previous_actions if action.task != "Exception"])
    return history
  
  def _run(
      self, 
      query: str = "", 
      chat_history: List[Tuple[str, str]] = [], 
      tasks_list: List[str] = [], 
      use_history: bool = False,
      **kwargs
    ) -> str:
    history = self._generate_history(chat_history=chat_history)
    # query += f"User: {message}"    
    # print(orchestrator.run("what is the name of the girlfriend of Leonardo Dicaperio?"))
    if self.sync_browser == None:
      self.sync_browser = create_sync_playwright_browser()

    if self.orchestrator == None:
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
        **kwargs
      )

    response, actions = self.orchestrator.run(query=query, history=history, meta=self.meta, use_history=use_history)
    self.previous_actions += actions

    return response

  def respond(
          self, 
          message, 
          chat_history, 
          check_box, 
          tasks_list
        ):
    print("hereee", self.previous_actions)
    response = self._run(query=message, chat_history=chat_history, tasks_list=tasks_list, use_history=check_box)
    chat_history.append((message, response))
    return "", chat_history
  
  def reset(self):
    self.previous_actions = []

  def run_with_interface(self):    
    available_tasks=[key.value for key in TASK_TO_CLASS.keys()]    
    interface = Interface()
    interface.prepare_interface(respond=self.respond, reset=self.reset, upload_meta=self.upload_meta, available_tasks=available_tasks)

  def upload_meta(self, history, file):
    history = history + [((file.name,), None)]
    self.meta.append(file.name)
    return history

  def run(
      self, 
      query: str = "", 
      chat_history: List[Tuple[str, str]] = [], 
      available_tasks: List[str] = [], 
      use_history:bool=False
    ) -> str:
    return self._run(query=query, chat_history=chat_history, tasks_list=available_tasks, use_history=use_history)

