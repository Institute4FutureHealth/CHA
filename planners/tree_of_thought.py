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
            """As a knowledgeable and empathetic health assistant, your primary objective is to provide the user with precise and valuable \
information regarding their health and well-being. Utilize the available tools effectively to answer health-related queries. \
Here are the tools at your disposal:
{tool_names}

Following is a general recommendation on how to call the tools to properly answer user query:
    1- Call needed tools to acquire data or information needed.
    2- Call needed analysis tools by providing requested information such as datapipe keys and retrieved infomartion.
    3- If the final results are stored in the datapipe, call `read_from_datapipe` task to get access to the raw data and use \
        it for your final answer. Make sure that you only read the needed data and not all the tools results. For example, \
        if you performed analysis on a sleep data, you should only read the result of the analysis and not the tool from step 2.

The following is the format of the information provided:
MetaData: this contains the name of data files of different types like image, audio, video, and text. You can pass these files to tools when needed.
History: the history of previous chats happened. Review the history for any previous responses relevant to the current query
PreviousActions: the list of already performed actions. You should start planning knowing that these actions are performed.
Question: the input question you must answer.

Considering previously executed actions and their results, use the tools and provided information, first suggest three \
strategies consisting of sequences of actions to properly answer the user query. Make sure the strategies are comprehensive enough \
and use proper tools.

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

PreviousActions:
{agent_scratchpad}

Tools:
{tool_names}

Using the selected final strategy mentioned in the 'Decision:\n', create a structured pseudo-code flow that outlines a \
sequence of steps. The flow should utilize predefined functions representing the tools available in a language \
model environment. If a step's output is required as input for a subsequent step, ensure the pseudo-code captures this dependency clearly. \
For each tool or function, include necessary parameters and assume each will return a result. If a step cannot be completed due to missing inputs, \
stop the flow at that point.
""",
        ]

    def task_descriptions(self):
        return "".join(
            [
                (
                    "\n-----------------------------------\n"
                    f"**{task.name}**: {task.description}"
                    "\nThis tool have the following outputs:\n"
                    "\n".join(task.outputs)(
                        "\n- The result of this tool will be stored in the datapipe."
                        if task.output_type
                        else ""
                    )
                    + "\n-----------------------------------\n"
                )
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

        pattern = r"([a-zA-Z_]+)\s*=\s*([a-zA-Z_]+)\(([^)]+)\)"

        # Find all matches in the pseudo code
        matches = re.findall(pattern, query)
        if len(matches) == 0:
            raise ValueError(
                "The tools should be called like functions with proper inputs and their result "
                "should be stored inside a variable."
            )
        actions = []
        for match in matches:
            tool_action = {
                "return_variable": match[0],
                "tool_name": match[1],
                "input_parameters": [
                    param.strip() for param in match[2].split(",")
                ],
            }
            actions.append(tool_action)

        return actions
