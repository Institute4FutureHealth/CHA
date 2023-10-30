from orchestrator.orchestrator import Orchestrator
from interface.base import Interface

  

interface = Interface()

orchestrator = Orchestrator.initialize(available_tasks=["serpapi"])
# print(orchestrator.run("what is the name of the girlfriend of Leonardo Dicaperio?"))

def respond(message, chat_history):
  query = "".join([f"User: {chat[0]}\nCHA: {chat[1]}\n" for chat in chat_history])
  # query += f"User: {message}"

  response = orchestrator.run(query=message, history=query, use_history=True)
  chat_history.append((message, response))
  return "", chat_history

interface.prepare_interface(respond=respond)