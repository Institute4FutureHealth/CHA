from planners.action import Action
from typing import List, Any
from orchestrator.orchestrator import Orchestrator
from interface.base import Interface
from tasks.types import TASK_TO_CLASS
from tasks.playwright.utils import create_sync_playwright_browser

class CHA:
  previous_actions: List[Action] = []
  sync_browser: Any = None

  def respond(self, message, chat_history, check_box, tasks_list):
    print("hereee", self.previous_actions)
    query = "".join([f"User: {chat[0]}\nCHA: {chat[1]}\n" for chat in chat_history])
    if len(self.previous_actions) > 0:
      query += "Previous Actions: " + "\n\n".join([f"action: {action.task}\naction_response: {action.task_response}" for action in self.previous_actions if action.task != "Exception"])
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

    response, actions = orchestrator.run(query=message, history=query, use_history=check_box)
    self.previous_actions += actions
    chat_history.append((message, response))
    return "", chat_history
  
  def reset(self):
    self.previous_actions = []

  def run_interface(self):    
    available_tasks=[key.value for key in TASK_TO_CLASS.keys()]    
    interface = Interface()
    interface.prepare_interface(respond=self.respond, reset=self.reset, available_tasks=available_tasks)