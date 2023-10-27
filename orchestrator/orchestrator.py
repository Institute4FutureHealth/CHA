from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from abc import abstractmethod
from planners.planner import BasePlanner
from planners.action import Action, PlanFinish
from datapipes.datapipe import DataPipe
from response_generators.response_generator import BaseResponseGenerator
from tasks.initialize_task import initialize_task
from planners.initialize_planner import initialize_planner
from datapipes.initialize_datapipe import initialize_datapipe

class Orchestrator():
  
  planner: BasePlanner = None
  datapipe: DataPipe = None
  promptist: Any = None 
  response_generator: BaseResponseGenerator = None
  available_tasks: List[str]

  role: int = 0

  def __init__(self, planner, datapipe, promptist, response_generator, available_tasks):
    self.planner = planner
    self.datapipe = datapipe
    self.promptist = promptist
    self.response_generator = response_generator
    self.available_tasks = available_tasks

  @classmethod
  def initialize(
        self, 
        planner_llm: str = "openai",
        planner: str = "zero-shot-react-planner", 
        datapipe: str = "memory",
        promptist: str = "",
        response_generator: str = "",
        generator_llm: str = "openai",
        available_tasks: List[str] = [],
        **kwargs
      ):
    planner = initialize_planner(tasks=available_tasks, llm=planner_llm, planner=planner, kwargs=kwargs)
    datapipe = initialize_datapipe(datapipe=datapipe)
    available_tasks = available_tasks
    return self(planner=planner, datapipe=datapipe, promptist=None, response_generator=None, available_tasks=available_tasks)



  def process_meta(self):
    return False 
  
  def execute_task(self, action):
    task = initialize_task(task=action.task)
    result = task.execute(action.task_input)
    if task.output_type:
      key = self.datapipe.store(result)
      return (
        f"The result of the task {task.name} is stored in the datapipe with key: {key}"
        "pass this key to other tasks to get access to the result."
      )
    return result

  def generate_prompt(self, query):
    return query 

  def plan(self, query):    
    return self.planner.plan(query)

  def generate_final_answer(self, query):
    return query

  def initialize_orchestrator(self):
    return self

  def run(
        self,
        query: str = "",
        meta: Any = {},
        use_history: bool = False,
        **kwargs: Any
      ) -> str: 
    prompt = self.generate_prompt(query)
    planner_intermediate_response = "\nObservation: "
    final_response = ""
    finished = False
    while True:
      actions = self.plan(prompt + "\nThougth:")
      for action in actions:
        if isinstance(action, PlanFinish):
          final_response = action.response
          finished = True
          break 
        else:
          planner_intermediate_response += self.execute_task(action)
          query += planner_intermediate_response
      if finished:
        break 
    final_response = self.generate_prompt(final_response)
    final_response = self.generate_final_answer(final_response)
    return final_response
      