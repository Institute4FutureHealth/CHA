from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import traceback 
from planners.planner import BasePlanner
from planners.action import Action, PlanFinish
from datapipes.datapipe import DataPipe
from response_generators.response_generator import BaseResponseGenerator
from tasks.initialize_task import initialize_task
from tasks.task import BaseTask
from planners.initialize_planner import initialize_planner
from datapipes.initialize_datapipe import initialize_datapipe
from response_generators.initialize_response_generator import initialize_response_generator
from pydantic import BaseModel

class Orchestrator(BaseModel):
  planner: BasePlanner = None
  datapipe: DataPipe = None
  promptist: Any = None 
  response_generator: BaseResponseGenerator = None
  available_tasks: Dict[str, BaseTask] = {}
  max_retries: int = 16
  max_task_execute_retries: int = 3
  max_planner_execute_retries: int = 3
  max_final_answer_execute_retries: int = 3
  role: int = 0

  @classmethod
  def initialize(
        self, 
        planner_llm: str = "openai",
        planner: str = "zero-shot-react-planner", 
        datapipe: str = "memory",
        promptist: str = "",
        response_generator: str = "base-generator",
        response_generator_llm: str = "openai",
        available_tasks: List[str] = [],
        **kwargs
      ) -> Orchestrator:
    tasks = {}      
    for task in available_tasks:
      tasks[task] = initialize_task(task=task, **kwargs)
    planner = initialize_planner(tasks=list(tasks.values()), llm=planner_llm, planner=planner, **kwargs)
    response_generator = initialize_response_generator(response_generator=response_generator, llm=response_generator_llm)
    datapipe = initialize_datapipe(datapipe=datapipe)
    return self(planner=planner, datapipe=datapipe, promptist=None, response_generator=response_generator, available_tasks=tasks)

  def process_meta(self) -> bool:
    return False 
  
  def execute_task(self, action) -> str:   
    retries = 0
    print("selected task", action)
    while retries < self.max_task_execute_retries:
      try:
        task = self.available_tasks[action.task] 
        result = task.execute(action.task_input)
        if task.output_type:
          key = self.datapipe.store(result)
          return (
            f"The result of the task {task.name} is stored in the datapipe with key: {key}"
            "pass this key to other tasks to get access to the result."
          )
        return result, task.return_direct
      except Exception as e:
        print(e)
        retries += 1
    return f"Error executing task {action.task}", False

  def generate_prompt(self, query) -> str:
    return query 

  def plan(self, query, history, previous_actions, use_history) -> List[Union[Action, PlanFinish]]:    
    retries = 0
    while retries < self.max_planner_execute_retries:
      try:
        return self.planner.plan(query, history, previous_actions, use_history)
      except Exception as e:
        print(e)
        retries += 1
    return [PlanFinish("Error planning, please try to ask your question again", "")]

  def generate_final_answer(self, query, thinker) -> str:
    retries = 0
    while retries < self.max_final_answer_execute_retries:
      try:
        return self.response_generator.generate(query=query, thinker=thinker)
      except Exception as e:
        print(e)
        retries += 1
    return "We currently have problem processing your question. Please try again after a while."
  
  def run(
        self,
        query: str = "",
        meta: Any = {},
        history: str = "",
        use_history: bool = False,
        **kwargs: Any
      ) -> str: 
    i = 0    
    previous_actions = []
    prompt = self.generate_prompt(query)
    if "google_translate" in self.available_tasks:
      prompt = self.available_tasks["google_translate"].execute(prompt+"$#en")
      source_language = prompt[1]
      prompt = prompt[0]
    # history = self.available_tasks["google_translate"].execute(history+"$#en").text
    final_response = ""
    finished = False
    while True:  
      try:    
        print(f"try {i}")
        actions = self.plan(query=prompt, history=history, previous_actions=previous_actions, use_history=use_history)
        for action in actions:
          if isinstance(action, PlanFinish):
            final_response = action.response
            finished = True
            break 
          else:          
            action.task_response, return_direct = self.execute_task(action)
            print("task response", action.task_response)
            previous_actions.append(action)
            if return_direct:
              final_response = action.task_response
              finished = True
            i = 0
        if finished:
          break 
      except ValueError as error:
        print("errrorr ", error)
        i += 1
        if i > self.max_retries:
          final_response = "Problem preparing the answer. Please try again."
          break
        previous_actions.append(Action("Exception", "Invalid or incomplete response", "".join(error.args), ""))

    final_response = self.generate_prompt(final_response)
    final_response = self.generate_final_answer(query=query, thinker=final_response)
    if "google_translate" in self.available_tasks:
      final_response =  self.available_tasks["google_translate"].execute(f"{final_response}$#{source_language}")[0]     
    return final_response, previous_actions
      