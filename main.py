from CHA import CHA

cha = CHA(verbose=True)
cha.run_with_interface()

# interface = Interface()
# available_tasks=["serpapi"]

# previous_actions = []

# def respond(message, chat_history, check_box, tasks_list):
#   print("hereee", previous_actions)
#   query = "".join([f"User: {chat[0]}\nCHA: {chat[1]}\n" for chat in chat_history])\
#           + " Previous Actions: " + "\n\n".join([f"action: {action.task}\naction_response: {action.task_response}" for action in previous_actions])
#   # query += f"User: {message}"
#   orchestrator = Orchestrator.initialize(available_tasks=tasks_list)
#   # print(orchestrator.run("what is the name of the girlfriend of Leonardo Dicaperio?"))
#   response, actions = orchestrator.run(query=message, history=query, use_history=check_box)
#   previous_actions = actions
#   chat_history.append((message, response))
#   return "", chat_history

# interface.prepare_interface(respond=respond, available_tasks=available_tasks)
