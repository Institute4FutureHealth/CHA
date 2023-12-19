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


class TreeOfThoughtPlanner(BasePlanner):
    """
    **Description:**

        This class implements Tree of Thought planner, which inherits from the BasePlanner base class.
        Tree of Thought employs parallel chain of thoughts startegies and decides which one is more
        suitable to proceed to get to the final answer.
        `Paper <https://arxiv.org/abs/2305.10601>`_

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
        return ["Wait"]

    @property
    def _planner_prompt(self):
        return [
            """You are very helpful empathetic health assistant and your goal is to help the user to get accurate information \
about his/her health and well-being. You have access to the following tools:
{tool_names}

The following is the format of the information provided:
MetaData: this contains the name of data files of different types like image, audio, video, and text. You can pass these files to tools when needed.
History: the history of previous chats happened. You should use them to answer user's current question. If the answer is already in the history,
just return it.
PreviousActions: the list of already performed actions. You should start planning knowing that these actions are performed.
Question: the input question you must answer.

Considering previous executed actions and their results, use the tools and provided information, suggest three unique creative \
sequences of actions to properly answer the user query. Here are list of rules that you should follow:
1- Use the provided tools only; no external actions are allowed.
2- Prioritize passing the datapipe key to other tools instead of using raw data.
3- Avoid calling the same tool with the same inputs from PreviousActions.
4- Start planning from previous actions.
5- If you want to use the result of another tool, mention it in the execute tool action.
6- Minimize the number of tool executions.
Then mention the pros and cons of each way. In the end decide the best strategy and write the detailed tool executions step by step.
start your final decision with
'Decision:\n'.

Begin!

MetaData: {meta}
History: {history}
PreviousActions: {agent_scratchpad}
Question: {input}
""",
            """
{strategy}
PreviousActions: {agent_scratchpad}
now based on your recommended strategy and previous actions, convert the steps into the following format. \
if an action is already executed and the result exist in previous actions, you do not need to call it again.
stick to the exact format:
Action: the action to take, SHOULD be only the tool name selected from one of [{tool_names}]
Action Inputs: the inputs should be seperated by $. Action inputs should be based on the input descriptions of the tool. \
The examples for a two input tasks are: input1$input2. If data pipe is needed make sure you prefix the key with `datapipe`
(...this action/action inputs can be repeated based on the steps you provided)
Wait: When response of a task needed.
Final Answer: When no further actions needed, provide the final answer to the original input question. It should be based on the tools result.
""",
        ]

    def task_descriptions(self):
        return "\n".join(
            [
                f"[tool name: {task.name}, description: {task.description}]"
                for task in self.available_tasks
            ]
        )

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
            Generate a plan using Tree of Thought

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
                    f"\nname: {action.task}\ninputs: {action.task_input}\nresult: {action.task_response}"
                    for action in previous_actions
                ]
            )
        prompt = (
            self._planner_prompt[0]
            .replace("{input}", query)
            .replace("{meta}", ", ".join(meta))
            .replace("{history}", history if use_history else "")
            .replace("{agent_scratchpad}", agent_scratchpad)
            .replace("{tool_names}", self.task_descriptions())
        )
        # if len(previous_actions) > 0:
        # prompt += "\nThought:"
        print(prompt)
        kwargs["max_tokens"] = 2000
        response = self._planner_model.generate(
            query=prompt, **kwargs
        )
        print("respp\n\n", response)
        prompt = (
            self._planner_prompt[1]
            .replace("{strategy}", response.split("Decision:\n")[-1])
            .replace("{tool_names}", self.get_available_tasks())
            .replace("{agent_scratchpad}", agent_scratchpad)
        )
        print("prompt2", prompt)
        kwargs["stop"] = self._stop
        response = self._planner_model.generate(
            query=prompt, **kwargs
        )

        index = min([response.find(text) for text in self._stop])
        response = response[0:index]
        print("resp", response)
        actions = self.parse(response)
        print("actions", actions)
        return actions

    def parse(
        self,
        query: str,
        **kwargs: Any,
    ) -> List[Union[Action, PlanFinish]]:
        """
            Parse the output query into a list of actions or a final answer. It parses the output based on \
            the following format:

                Action: action\n
                Action Inputs: inputs

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
            r"(" + "|".join(self.get_available_tasks_list()) + r")"
        )
        regex = (
            r"\s*Action\s*\d*\s*:[\s]*.*?"
            + str_pattern
            + r".*?[\s]*Action\s*\d*\s*Inputs\s*\d*\s*:[\s]*(.*)"
        )

        action_matches = re.findall(regex, query)
        print("actions matched", action_matches)
        if (
            len(action_matches) > 0
            and includes_answer
            and query.find(action_matches[-1][-1])
            > query.find(FINAL_ANSWER_ACTION)
        ):
            raise ValueError(
                "Parsing the output produced both a final answer and a parse-able action."
            )

        actions = []
        if len(action_matches) > 0:
            print("heree")
            for match in action_matches:
                actions.append(Action(match[0], match[1], "", ""))
        if includes_answer:
            actions.append(
                PlanFinish(
                    query.split(FINAL_ANSWER_ACTION)[-1].strip(),
                    "",
                )
            )

        if len(actions) > 0:
            return actions

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
