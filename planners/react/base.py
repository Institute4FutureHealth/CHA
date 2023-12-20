"""
Heavily borrowed from langchain: https://github.com/langchain-ai/langchain/
"""
import re
from typing import Any
from typing import List
from typing import Union

from planners.action import Action
from planners.action import PlanFinish
from planners.planner import BasePlanner


class ReActPlanner(BasePlanner):
    """
    **Description:**

        This class implements ReAct planner, which inherits from the BasePlanner base class.
        ReAct employs reasoning and action techniques to ascertain the essential actions to be undertaken.
        `Paper <https://arxiv.org/abs/2210.03629>`_

        This code defines a base class called "BasePlanner" that inherits from the "BaseModel" class of the pydantic library.
        The BasePlanner class serves as a base for implementing specific planners.


    """

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    @property
    def _planner_type(self):
        return "zero-shot-react-planner"

    @property
    def _planner_model(self):
        return self.llm_model

    @property
    def _stop(self) -> List[str]:
        return ["Observation"]

    @property
    def _planner_prompt(self):
        return """You are very helpful empathetic health assistant and your goal is to help the user to get accurate information \
about his/her health and well-being. Answer the following questions as best you can. Make sure you call all the needed tools before \
reach to the Final Answer.
Here are list of rules that you should follow:
1- Avoid calling the same tool with the same inputs from PreviousActions.
2- If you want to use the result of another tool, mention it in the execute tool action.
3- Minimize the number of tool executions.
4- You should try your best to pass datapipe data to other tools and avoid analysing data by yourself. Worst case read raw data from datapipe and \
use it to answer the user's query.
5- when your Thought is 'I now know the final answer' you should provide 'Final Answer:'
6- When data in the datapipe requires analysis without numerical calculations. Please prioritize using tools for any \
data-related tasks. Provide guidance on how to use the available tools effectively.
7- you should be fully aware of what you are doing and based on the history and previous tools used, you should decide \
what inputs should be provided to other tools. for example if you already fetched a user data in the next tools you should \
provide data based on this knowledge.

Use the following format. You should stick to the following format:
MetaData: this contains the name of data files of different types like image, audio, video, and text. You can pass these files to tools when needed.
History: the history of previous chats happened. You should use them to answer user's current question. If the answer is already in the history, \
just return it.
Question: the input question you must answer
Thought: you should always think about what to do. Describe what you want to do and then select actions.
Action: the action to take, SHOULD be only the tool name selected from one of [{tool_names}]
Action Inputs: the inputs should be seperated by $. Action inputs should be based on the input descriptions of the tool. \
The examples for a two input tools are: input1$input2 or if datapipe is needed datapipe:key$input2
Observation: the result of the action
... (this Thought/Action/Action Inputs/Observation can repeat N times)
Thought: Your final reasoning or 'I now know the final answer'. when you think you are done you should provide the 'Final Answer'.
Final Answer: the final answer to the original input question. It should be based on the tools result.

Begin!

MetaData: {meta}
History: {history}
Question: {input}
Thought: {agent_scratchpad}"""

    def plan(
        self,
        query: str,
        history: str = "",
        meta: str = "",
        previous_actions: List[Action] = None,
        use_history: bool = False,
        **kwargs: Any,
    ) -> List[Union[Action, PlanFinish]]:
        """
            Generate a plan using ReAct

        Args:
            query (str): Input query.
            history (str): History information.
            meta (str): meta information.
            previous_actions (List[Action]): List of previous actions.
            use_history (bool): Flag indicating whether to use history.
            **kwargs (Any): Additional keyword arguments.
        Return:
            Action: return action.

        """
        if previous_actions is None:
            previous_actions = []

        agent_scratchpad = ""
        if len(previous_actions) > 0:
            agent_scratchpad = "\n".join(
                [
                    f"Action: {action.task}\nAction Inputs: {action.task_input}\nObservation: {action.task_response}\nThought:"
                    for action in previous_actions
                ]
            )
        prompt = (
            self._planner_prompt.replace("{input}", query)
            .replace("{meta}", ", ".join(meta))
            .replace("{history}", history if use_history else "")
            .replace("{agent_scratchpad}", agent_scratchpad)
            .replace("{tool_names}", self.get_available_tasks())
        )
        print("prompt", prompt)
        # if len(previous_actions) > 0:
        # prompt += "\nThought:"
        kwargs["max_tokens"] = 500
        kwargs["stop"] = self._stop
        response = self._planner_model.generate(
            query=prompt, **kwargs
        )
        index = min([response.find(text) for text in self._stop])
        index1 = response.find("\nAction:")
        if index1 == -1:
            index1 = 0
        print("resp", response)
        response = response[index1:index]
        actions = self.parse(response)
        return actions

    def parse(
        self,
        query: str,
        **kwargs: Any,
    ) -> List[Union[Action, PlanFinish]]:
        """
            Parse the output query into a list of actions or a final answer. It parses the output based on \
            the following format:

                Thought: though\n
                Action: action\n
                Action Inputs: inputs

                or


                Thought: though\n
                Final Answer: final answer\n


        Args:\n
            query (str): The planner output query to extract actions.
            **kwargs (Any): Additional keyword arguments.
        Return:
            List[Union[Action, PlanFinish]]: List of parsed actions or a finishing signal.
        Raise:
            ValueError: If parsing encounters an invalid format or unexpected content.

        """

        FINAL_ANSWER_ACTION = "Final Answer:"
        includes_answer = FINAL_ANSWER_ACTION in query
        str_pattern = (
            r"(?:"
            + "|".join(self.get_available_tasks_list())
            + r")(?=.*Action\s*\d*\s*Inputs)"
        )
        regex = (
            r"\s*Action\s*\d*\s*:[\s]*.*?("
            + str_pattern
            + r").*?[\s]*Action\s*\d*\s*Inputs\s*\d*\s*:[\s]*(.*)"
        )

        action_match = re.search(regex, query, re.DOTALL)
        if action_match and includes_answer:
            if query.find(FINAL_ANSWER_ACTION) < query.find(
                action_match.group(0)
            ):
                # if final answer is before the hallucination, return final answer
                start_index = query.find(FINAL_ANSWER_ACTION) + len(
                    FINAL_ANSWER_ACTION
                )
                end_index = query.find("\n\n", start_index)
                return [
                    PlanFinish(query[start_index:end_index].strip())
                ]
            else:
                raise ValueError(
                    "Parsing the output produced both a final answer and a parse-able action."
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
            return [
                PlanFinish(
                    query.split(FINAL_ANSWER_ACTION)[-1].strip(),
                    query,
                )
            ]

        if not re.search(
            r"Action\s*\d*\s*:[\s]*.*?(" + str_pattern + r").*?",
            query,
            re.DOTALL,
        ):
            raise ValueError(
                "Invalid Format: Missing 'Action:' or 'Final Answer' after 'Thought:'\n"
                # f"Or The tool name is wrong. The tool name should be one of: `{self.get_available_tasks_list()}`"
            )
        elif not re.search(
            r"[\s]*Action\s*\d*\s*Inputs\s*\d*\s*:[\s]*(.*)",
            query,
            re.DOTALL,
        ):
            raise ValueError(
                "Invalid Format: Missing 'Action Input:' after 'Action:'"
            )
        else:
            raise ValueError("Wrong format.")
