from orchestrator.orchestrator import Orchestrator

orchestrator = Orchestrator.initialize(available_tasks=["serpapi"])
print(orchestrator.run("what is the name of the girlfriend of Leonardo Dicaperio?"))