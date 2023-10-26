"""
Heavily borrowed from langchain: https://github.com/langchain-ai/langchain/
"""
from planners.planner import BasePlanner
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from action import Action, PlanFinish
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
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Inputs: the comma seperated inputs to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

  def get_available_tasks(self) -> Optional[List[str]]:
    return self.available_tools
  
  def plan(
        self,
        query: str,
        **kwargs: Any,
      ) -> List[Action]:
    response = self._planner_model.generate(query)
    index = min([response.rfind(text) for text in self._stop])
    response = response[:index]
    actions = self.parse(response)
    return actions    


  def parse(
        self,
        query: str,
        **kwargs: Any,
      ) -> List[Action]:
    FINAL_ANSWER_ACTION = "Final Answer:"
    includes_answer = FINAL_ANSWER_ACTION in query
    regex = (
        r"Action\s*\d*\s*:[\s]*(.*?)[\s]*Action\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
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

        return Action(action, tool_input, query)

    elif includes_answer:
        return PlanFinish(
            {"output": query.split(FINAL_ANSWER_ACTION)[-1].strip()}, query
        )

    if not re.search(r"Action\s*\d*\s*:[\s]*(.*?)", query, re.DOTALL):
        raise ValueError(
            f"Could not parse LLM output: `{query}`",
            observation="Invalid Format: Missing 'Action:' after 'Thought:'",
            llm_output=query,
            send_to_llm=True,
        )
    elif not re.search(
        r"[\s]*Action\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)", query, re.DOTALL
    ):
        raise ValueError(
            f"Could not parse LLM output: `{query}`",
            observation="Invalid Format:"
            " Missing 'Action Input:' after 'Action:'",
            llm_output=query,
            send_to_llm=True,
        )
    else:
        raise ValueError(f"Could not parse LLM output: `{query}`")