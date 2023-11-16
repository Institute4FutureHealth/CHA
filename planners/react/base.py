"""
Heavily borrowed from langchain: https://github.com/langchain-ai/langchain/
"""
from planners.planner import BasePlanner
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from planners.action import Action, PlanFinish
import re


class ReActPlanner(BasePlanner):
    """ReActPlanner"""

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

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
        return """You are very helpful empathetic health assistant and your goal is to help the user to get accurate information about his/her health and well-being. 
Answer the following questions as best you can. You have access to the following tools:
Use the following format. You should stick to the following format:
Question: the input question you must answer
MetaData: this contains the name of data files of different types like image, audio, video, and text. You can pass these files to tools when needed.
History: the history of previous chats happened. You should use them to answer user's current question. If the answer is already in the history, just return it.
Thought: you should always think about what to do. Ask yourself how to break down the Question into actions using tools. you may need to call tools several times for different purposes. 
Action: the action to take, SHOULD be only the tool name selected from one of [{tool_names}]
Action Inputs: the comma seperated inputs to the action should be based on the input descriptions of the task
Observation: the result of the action
... (this Thought/Action/Action Inputs/Observation can repeat N times)
Thought: Your final reasoning or 'I now know the final answer'. when you think you are done provide the 'Final Answer'. You can use the final thoughts directly in the final answer.
Final Answer: the final answer to the original input question

Begin!

Question: {input}
MetaData: {meta}
History: {history}
Thought: {agent_scratchpad}"""


def plan(
        self,
        query: str,
        history: str = "",
        meta: str = "",
        previous_actions: List[Action] = [],
        use_history: bool = False,
        **kwargs: Any,
) -> List[Union[Action, PlanFinish]]:
    """
    Generate a plan based on the input query, history, and previous actions.

    Args:
        query (str): Input query.
        history (str): History information.
        meta (str): meta information.
        previous_actions (List[Action]): List of previous actions.
        use_history (bool): Flag indicating whether to use history.
        **kwargs (Any): Additional keyword arguments.
    Return:
        Action: return action.



    Example:
        .. code-block:: python

            from langchain import ReActChain, OpenAI
            react = ReAct(llm=OpenAI())

    """


    agent_scratchpad = ""
    if len(previous_actions) > 0:
        agent_scratchpad = "\n".join([
            f"Action: {action.task}\nAction Inputs: {action.task_input}\nObservation: {action.task_response}\nThought:"
            for action in previous_actions
        ])
    prompt = self._planner_prompt.replace("{input}", query) \
        .replace("{meta}", meta) \
        .replace("{history}", history if use_history else "") \
        .replace("{agent_scratchpad}", agent_scratchpad) \
        .replace("{tool_names}", self.get_available_tasks())
    # if len(previous_actions) > 0:
    # prompt += "\nThought:"

    kwargs["max_tokens"] = 150
    kwargs["stop"] = self._stop
    response = self._planner_model.generate(query=prompt, **kwargs)

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
    """
    Parse the output query into a list of actions or a final answer.

    Args:
        query (str): Output query.
        **kwargs (Any): Additional keyword arguments.
    Return:
        List[Union[Action, PlanFinish]]: List of parsed actions or a finishing signal.
    Raise:
        ValueError: If parsing encounters an invalid format or unexpected content.



    Example:
        .. code-block:: python

            from langchain import ReActChain, OpenAI
            react = ReAct(llm=OpenAI())

    """

    FINAL_ANSWER_ACTION = "Final Answer:"
    includes_answer = FINAL_ANSWER_ACTION in query
    str_pattern = "(?:" + "|".join(self.get_available_tasks_list()) + ")(?=.*Action\s*\d*\s*Inputs)"
    regex = (
            r"\s*Action\s*\d*\s*:[\s]*.*?(" + str_pattern + r").*?[\s]*Action\s*\d*\s*Inputs\s*\d*\s*:[\s]*(.*)"
    )


    action_match = re.search(regex, query, re.DOTALL)
    if action_match and includes_answer:
        if query.find(FINAL_ANSWER_ACTION) < query.find(action_match.group(0)):
            # if final answer is before the hallucination, return final answer
            start_index = query.find(FINAL_ANSWER_ACTION) + len(FINAL_ANSWER_ACTION)
            end_index = query.find("\n\n", start_index)
            return PlanFinish(
                query[start_index:end_index].strip()
            )
        else:
            raise ValueError(
                f"Parsing the output produced both a final answer and a parse-able action."
            )

    if action_match:
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
            "Invalid Format: Missing 'Action:' or 'Final Answer' after 'Thought:'\n"
            # f"Or The tool name is wrong. The tool name should be one of: `{self.get_available_tasks_list()}`"
        )
    elif not re.search(
            r"[\s]*Action\s*\d*\s*Inputs\s*\d*\s*:[\s]*(.*)", query, re.DOTALL
    ):
        raise ValueError(
            "Invalid Format: Missing 'Action Input:' after 'Action:'"
        )
    else:
        raise ValueError(f"Wrong format.")
