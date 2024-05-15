from __future__ import annotations

import uuid
from typing import Any
from typing import List

from pydantic import BaseModel

from datapipes.datapipe import DataPipe
from tasks.task import OutputType


class Action(BaseModel):
    """
    **Description:**

    The executed tasks and their results will be stored as actions. These actions are used to create Previous Actions part of the prompts
    or to serve as a cache for preventing executing same tasks multiple times improving latency.
    """

    id: str = str(uuid.uuid4())
    task_name: str = ""
    task_inputs: List[str] = None
    task_response: Any = None
    task_outputs: List[str] = None
    output_type: OutputType = OutputType.LLM_TEXT
    datapipe: DataPipe = None

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def dict(self, return_result: bool = False):
        response = self.task_response
        if (
            self.output_type == OutputType.DATAPIPE
        ) and return_result:
            response = self.datapipe.retrieve(
                response.split("datapipe:")[-1]
            )

        return (
            "\n------------------\n"
            f"{self.task_name}: {self.task_inputs}\n"
            f"Output: {self.task_outputs}\n"
            f"{response}"
            "\n------------------\n"
        )
