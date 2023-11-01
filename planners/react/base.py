"""
Heavily borrowed from langchain: https://github.com/langchain-ai/langchain/
"""
from planners.planner import BasePlanner
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from planners.action import Action, PlanFinish
import re

class ReActPlanner(BasePlanner):
  """ReActPlanner"""

  @property
  def _planner_type(self):
    raise "zero-shot-react-planner"

  @property
  def _planner_model(self):
    return self.llm_model

  @property
  def _stop(self) -> List[str]:
    return ["Observation"]

  @property
  def _planner_prompt(self):
    return """Answer the following questions as best you can. You have access to the following tools:
Use the following format:
Question: the input question you must answer
History: the history of previous chats happened. You should use them to answer user's current question.
Thought: you should always think about what to do
Action: the action to take, SHOULD be only the tool name selected from one of [{tool_names}]
Action Inputs: the comma seperated inputs to the action
Observation: the result of the action
... (this Thought/Action/Action Inputs/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
History: {history}
Thought: {agent_scratchpad}"""  

  def plan(
        self,
        query: str,
        history: str,
        previous_actions: List[Action],
        use_history: bool = False,
        **kwargs: Any,
      ) -> List[Union[Action, PlanFinish]]:

    agent_scratchpad = ""
    if len(previous_actions) > 0:
      agent_scratchpad = "\n".join([
        f"Action: {action.task}\nAction Inputs: {action.task_input}\nObservation: {action.task_response}"
        for action in previous_actions
      ])
    prompt = self._planner_prompt.replace("{input}", query)\
                                  .replace("{history}", history if use_history else "")\
                                  .replace("{agent_scratchpad}", agent_scratchpad)\
                                  .replace("{tool_names}", self.get_available_tasks())
    # if len(previous_actions) > 0:
      # prompt += "\nThought:"

    print("prompt ", prompt, "\n")
    response = self._planner_model.generate(query=self.prepare_prompt(prompt), kwargs=kwargs)
    print("response ", response, "\n")

    index = min([response.find(text) for text in self._stop])
    index1 = response.find("\nAction:")
    if index1 == -1:
       index1 = 0
    response = response[index1:index]
    actions = self.parse(response)
    return actions    


  def parse(
        self,
        query: str,
        **kwargs: Any,
      ) -> List[Union[Action, PlanFinish]]:
    FINAL_ANSWER_ACTION = "Final Answer:"
    includes_answer = FINAL_ANSWER_ACTION in query
    str_pattern = "(?:" + "|".join(self.get_available_tasks_list()) + ")(?=.*Action\s*\d*\s*Inputs)"    
    regex = (
         r"Action\s*\d*\s*:[\s]*.*?(" + str_pattern + r").*?[\s]*Action\s*\d*\s*Inputs\s*\d*\s*:[\s]*(.*)"
    )
    action_match = re.search(regex, query, re.DOTALL)
    if action_match:
        if includes_answer:
            raise ValueError(
                "Parsing LLM output produced both a final answer "
                f"and a parse-able action: {query}"
            )

        action = action_match.group(1).strip()
        action_input = action_match.group(2)
        tool_input = action_input.strip(" ")
        # ensure if its a well formed SQL query we don't remove any trailing " chars
        if tool_input.startswith("SELECT ") is False:
            tool_input = tool_input.strip('"')

        return [Action(action, tool_input, "", query)]

    elif includes_answer:
        return [PlanFinish(
            query.split(FINAL_ANSWER_ACTION)[-1].strip(), query
        )]

    if not re.search(r"Action\s*\d*\s*:[\s]*.*?(" + str_pattern + r").*?", query, re.DOTALL):
        raise ValueError(
            f"Could not parse LLM output: `{query}`",
            "Invalid Format: Missing 'Action:' after 'Thought:'",
            query,
        )
    elif not re.search(
        r"[\s]*Action\s*\d*\s*Inputs\s*\d*\s*:[\s]*(.*)", query, re.DOTALL
    ):
        raise ValueError(
            f"Could not parse LLM output: `{query}`",
            "Invalid Format:",
            " Missing 'Action Input:' after 'Action:'",
            query
        )
    else:
        raise ValueError(f"Could not parse LLM output: `{query}`")