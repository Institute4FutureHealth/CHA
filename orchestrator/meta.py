from __future__ import annotations

import uuid
from typing import List

from pydantic import BaseModel

from datapipes.datapipe import DataPipe


class Meta(BaseModel):
    """
    **Description:**

    The meta data that is recieved by user like audio, video, image or the generated audio, video, and image with necessary \
    information and description will be kept as Meta object.
    """

    id: str = str(uuid.uuid4())
    path: str = ""
    type: str = ""
    description: str = ""
    tag: str = ""
    tasks_already_run: List[str] = []

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def add_task(self, task_name):
        self.tasks_already_run.append(task_name)

    def dict(self):
        return (
            "\n------------------\n"
            f"id: {self.id}\n"
            f"filename: {self.path.split('/')[-1]}\n"
            f"file_type: {self.type}\n"
            f"tag: {self.tag}\n"
            f"description: {self.description}\n"
            f"The following tasks are already performed. You should not call them again for this meta data: {self.tasks_already_run}"
            "\n------------------\n"
        )
