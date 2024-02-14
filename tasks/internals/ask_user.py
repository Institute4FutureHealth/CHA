from typing import Any
from typing import List

from tasks.task import BaseTask


class AskUser(BaseTask):
    """
    **Description:**

        This task is asking question back to the user and stops planning. When needed, the planner will decide to ask question from user
        and use the user's answer to proceed to the planning.

    """

    name: str = "ask_user"
    chat_name: str = "AskUser"
    description: str = (
        "This task can be used when there is ambiguity in the users' query or more information is needed to be gathered from user. "
        "When there is no task to call, you should call this task."
    )
    dependencies: List[str] = []
    inputs: List[str] = ["The text returned to user."]
    outputs: List[str] = []
    output_type: bool = False
    return_direct: bool = True

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        """Translate query"""
        if inputs is None:
            return ""
        return inputs[0]

    def explain(
        self,
    ) -> str:
        return "This task simply asks user to provide more information or continue interaction."
