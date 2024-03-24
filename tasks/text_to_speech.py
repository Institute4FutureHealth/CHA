import uuid
from typing import Any
from typing import Dict
from typing import List

from pydantic import model_validator

from tasks.task import BaseTask
from tasks.task import OutputType


class TextToSpeech(BaseTask):
    """
    **Description:**

        This task is converts user audio into text to start planning and answering.

    """

    name: str = "text_to_speech"
    chat_name: str = "TextToSpeech"
    description: str = "This task converts text into speech."
    dependencies: List[str] = []
    inputs: List[str] = [
        "The text to be converted.",
        "The text language.",
    ]
    outputs: List[str] = [
        "The output is the speech file of the input text."
    ]
    output_type: OutputType = OutputType.METADATA
    return_direct: bool = False
    executor_task: bool = True
    gtts: Any = None

    @model_validator(mode="before")
    def validate_environment(cls, values: Dict) -> Dict:
        """
            Validate that api key and python package exists in environment.

        Args:
            values (Dict): The dictionary of attribute values.
        Return:
            Dict: The updated dictionary of attribute values.
        Raise:
            ValueError: If the SerpAPI python package is not installed.

        """

        try:
            from gtts import gTTS

            values["gtts"] = gTTS
        except ImportError:
            raise ValueError(
                "Could not import transformers python package. "
                "Please install it with `pip install gtts`."
            )
        return values

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        tts = self.gtts(inputs[0], lang=inputs[1])
        filename = f"./data/{str(uuid.uuid4())}.mp3"
        tts.save(filename)
        return filename

    def explain(
        self,
    ) -> str:
        return "This task uses Whisper as speech to text module."
