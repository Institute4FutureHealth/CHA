from planners.action import Action
from typing import List
from orchestrator.orchestrator import Orchestrator
from interface.base import Interface

class CHA:
  previous_actions: List[Action] = []

  def respond(self, message, chat_history, check_box, tasks_list):
    print("hereee", self.previous_actions)
    query = "".join([f"User: {chat[0]}\nCHA: {chat[1]}\n" for chat in chat_history])
    if len(self.previous_actions) > 0:
      query += "Previous Actions: " + "\n\n".join([f"action: {action.task}\naction_response: {action.task_response}" for action in self.previous_actions])
    # query += f"User: {message}"
    orchestrator = Orchestrator.initialize(available_tasks=tasks_list)
    # print(orchestrator.run("what is the name of the girlfriend of Leonardo Dicaperio?"))
    response, actions = orchestrator.run(query=message, history=query, use_history=check_box)
    self.previous_actions += actions
    chat_history.append((message, response))
    return "", chat_history

  def run_interface(self):
    interface = Interface()
    available_tasks=["serpapi"]
    interface.prepare_interface(respond=self.respond, available_tasks=available_tasks)