from __future__ import annotations

import uuid

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
    datapipe: DataPipe = None

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def dict(self):
        response = self.task_response

        return (
            "\n------------------\n"
            f"{self.task_name}: {self.task_inputs}\n"
            f"{response}"
            "\n------------------\n"
        )
