from planners.action import Action
from typing import List, Any, Tuple
from orchestrator.orchestrator import Orchestrator
from interface.base import Interface
from tasks.types import TASK_TO_CLASS
from tasks.playwright.utils import create_sync_playwright_browser
from pydantic import BaseModel

class CHA(BaseModel):
  previous_actions: List[Action] = []
  sync_browser: Any = None

  def _generate_history(self, chat_history: List[Tuple[str, str]]=[]):
    history = "".join([f"User: {chat[0]}\nCHA: {chat[1]}\n" for chat in chat_history])
    if len(self.previous_actions) > 0:
      history += "Previous Actions: " + "\n\n".join([f"action: {action.task}\naction_response: {action.task_response}" for action in self.previous_actions if action.task != "Exception"])
    return history
  
  def _run(self, query: str="", chat_history: List[Tuple[str, str]]=[], tasks_list: List[str]=[], use_history: bool=False):
    history = "".join([f"User: {chat[0]}\nCHA: {chat[1]}\n" for chat in chat_history])
    if len(self.previous_actions) > 0:
      history += "Previous Actions: " + "\n\n".join([f"action: {action.task}\naction_response: {action.task_response}" for action in self.previous_actions if action.task != "Exception"])
    # query += f"User: {message}"    
    # print(orchestrator.run("what is the name of the girlfriend of Leonardo Dicaperio?"))
    if self.sync_browser == None:
      self.sync_browser = create_sync_playwright_browser()

    orchestrator = Orchestrator.initialize(      
      planner_llm="openai",
      planner="zero-shot-react-planner", 
      datapipe="memory",
      promptist="",
      response_generator="base-generator",
      response_generator_llm="openai",
      available_tasks=tasks_list, 
      sync_browser=self.sync_browser
    )

    response, actions = orchestrator.run(query=query, history=history, use_history=use_history)
    self.previous_actions += actions

    return response

  def respond(self, message, chat_history, check_box, tasks_list):
    print("hereee", self.previous_actions)
    response = self._run(self, query=message, chat_history=chat_history, tasks_list=tasks_list, use_history=check_box)
    chat_history.append((message, response))
    return "", chat_history
  
  def reset(self):
    self.previous_actions = []

  def run_with_interface(self):    
    available_tasks=[key.value for key in TASK_TO_CLASS.keys()]    
    interface = Interface()
    interface.prepare_interface(respond=self.respond, reset=self.reset, available_tasks=available_tasks)

  def run(self, query:str = "", chat_history: List[Tuple[str, str]]=[], use_history:bool=False):
    available_tasks=[key.value for key in TASK_TO_CLASS.keys()]
    self._run(query, )

