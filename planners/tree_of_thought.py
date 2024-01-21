"""
Heavily borrowed from langchain: https://github.com/langchain-ai/langchain/
"""
import re
from typing import Any
from typing import List

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

    summarize_prompt: bool = True
    max_tokens_allowed: int = 10000

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
    def _response_generator_model(self):
        return self.llm_model

    @property
    def _stop(self) -> List[str]:
        return ["Wait"]

    @property
    def _shorten_prompt(self):
        return (
            "Summarize the following text. Make sure to keep the main ideas "
            "and objectives in the summary. Keep the links "
            "exactly as they are: "
            "{chunk}"
        )

    @property
    def _planner_prompt(self):
        return [
            """As a knowledgeable and empathetic health assistant, your primary objective is to provide the user with precise and valuable \
information regarding their health and well-being. Utilize the available tools effectively to answer health-related queries. \
Here are the tools at your disposal:
{tool_names}

The following is the format of the information provided:
MetaData: this contains the name of data files of different types like image, audio, video, and text. You can pass these files to tools when needed.
History: the history of previous chats happened. Review the history for any previous responses relevant to the current query
PreviousActions: the list of already performed actions. You should start planning knowing that these actions are performed.
Question: the input question you must answer.

Considering previously actions and their results, use the tools and provided information, first suggest three \
creative strategies with detailed explanation consisting of sequences of tools to properly answer the user query. \
Make sure the strategies are comprehensive enough and use proper tools. The tools constraints should be always satisfied. \

After specifying the strategies, mention the pros and cons of each strategy. \
In the end decide the best strategy and write the detailed tool executions step by step.
start your final decision with
'Decision:'.

Begin!

MetaData:
{meta}
=========================
History:
{history}
=========================
{previous_actions}
=========================
Question: {input}
""",
            """
{strategy}
=========================
{previous_actions}
=========================
Tools:
{tool_names}
=========================

You are skilled python programmer that can solve problems and convert them into python codes. \
Using the selected final strategy mentioned in the 'Decision:
', create a python code inside a ```python ``` block that outlines a sequence of steps using the Tools. \
assume that there is an **self.execute_task** function that can execute the tools in it. The execute_task \
recieves task name and an array of the inputs and returns the result. Make sure that you always pass and array as second argument. \
You can call tools like this: \
**task_result = self.execute_task('tool_name', ['input_1', 'input2', ...])**. \
The flow should utilize this style representing the tools available. Make sure all the execute_task calls outputs are stored in a variable.\
If a step's output is required as input for a subsequent step, ensure the python code captures this dependency clearly. \
The output variables should directly passed as inputs with no changes in the wording.
If the tool input is a datapipe only put the variable as the input. \
For each tool, include necessary parameters directly without any names and assume each will return an output. \
The outputs' description are provided for each Tool individually. Make sure you use the directives when passing the outputs.
""",
        ]

    def task_descriptions(self):
        return "".join(
            [
                (
                    "\n-----------------------------------\n"
                    f"**{task.name}**: {task.description}"
                    "\nThis tool have the following outputs:\n"
                    + "\n".join(task.outputs)
                    + (
                        "\n- The result of this tool will be stored in the datapipe."
                        if task.output_type
                        else ""
                    )
                    + "\n-----------------------------------\n"
                )
                for task in self.available_tasks
            ]
        )

    def divide_text_into_chunks(
        self,
        input_text: str = "",
        max_tokens: int = 10000,
    ) -> List[str]:
        """
        Generate a response based on the input prefix, query, and thinker (task planner).

        Args:
            input_text (str): the input text (e.g., prompt).
            max_tokens (int): Maximum number of tokens allowed.
        Return:
            chunks(List): List of string variables
        """
        # 1 token ~= 4 chars in English
        chunks = [
            input_text[i : i + max_tokens * 4]
            for i in range(0, len(input_text), max_tokens * 4)
        ]
        return chunks

    def generate_scratch_pad(
        self, previous_actions: List[str] = None, **kwargs: Any
    ):
        if previous_actions is None:
            previous_actions = []

        agent_scratchpad = ""
        if len(previous_actions) > 0:
            agent_scratchpad = "\n".join(
                [f"\n{action}" for action in previous_actions]
            )
        # agent_scratchpad
        if (
            self.summarize_prompt
            and len(agent_scratchpad) / 4 > self.max_tokens_allowed
        ):
            # Shorten agent_scratchpad
            chunks = self.divide_text_into_chunks(
                input_text=agent_scratchpad,
                max_tokens=self.max_tokens_allowed,
            )
            agent_scratchpad = ""
            kwargs["max_tokens"] = min(
                2000, int(self.max_tokens_allowed / len(chunks))
            )
            for chunk in chunks:
                prompt = self._shorten_prompt.replace(
                    "{chunk}", chunk
                )
                chunk_summary = (
                    self._response_generator_model.generate(
                        query=prompt, **kwargs
                    )
                )
                agent_scratchpad += chunk_summary + " "

    def plan(
        self,
        query: str,
        history: str = "",
        meta: str = "",
        previous_actions: List[str] = None,
        use_history: bool = False,
        **kwargs: Any,
    ) -> str:
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

        previous_actions_prompt = ""
        if len(previous_actions) > 0 and self.use_previous_action:
            previous_actions_prompt = f"Previoius Actions:\n{self.generate_scratch_pad(previous_actions, **kwargs)}"

        prompt = (
            self._planner_prompt[0]
            .replace("{input}", query)
            .replace("{meta}", ", ".join(meta))
            .replace(
                "{history}", history if use_history else "No History"
            )
            .replace("{previous_actions}", previous_actions_prompt)
            .replace("{tool_names}", self.task_descriptions())
        )
        # if len(previous_actions) > 0:
        # prompt += "\nThought:"
        print(prompt)
        kwargs["max_tokens"] = 1000
        response = self._planner_model.generate(
            query=prompt, **kwargs
        )
        print("respp\n\n", response)
        prompt = (
            self._planner_prompt[1]
            .replace(
                "{strategy}",
                "Decision:\n" + response.split("Decision:")[-1],
            )
            .replace("{tool_names}", self.get_available_tasks())
            .replace("{previous_actions}", previous_actions_prompt)
        )
        print("prompt2", prompt)
        kwargs["stop"] = self._stop
        response = self._planner_model.generate(
            query=prompt, **kwargs
        )

        index = min([response.find(text) for text in self._stop])
        response = response[0:index]
        actions = self.parse(response)
        print("actions", actions)
        return actions

    def parse(
        self,
        query: str,
        **kwargs: Any,
    ) -> str:
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
        pattern = r"`+python\n(.*?)`+"
        code = re.search(pattern, query, re.DOTALL).group(1)
        return code
