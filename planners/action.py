from dataclasses import dataclass


@dataclass
class Action:
    task: str
    task_input: str
    task_response: str
    log: str


@dataclass
class PlanFinish:
    response: dict
    log: str
