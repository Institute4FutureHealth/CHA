from typing import Any
from typing import Dict
from typing import List

import numpy as np
from pydantic import Extra
from pydantic import model_validator
from scipy.io import wavfile

from tasks.task import BaseTask


class AudioToText(BaseTask):
    """
    **Description:**

        This task is converts user audio into text to start planning and answering.

    """

    name: str = "audio_to_text"
    chat_name: str = "AudioToText"
    description: str = (
        "This task converts audio into text. It support wav and mp3 file extention. "
        "You should use this task only if inside the Meta Data there are some audio files with .wav suffix."
    )
    dependencies: List[str] = []
    inputs: List[str] = ["The meta data id of the audio path."]
    outputs: List[str] = []
    output_type: bool = False
    return_direct: bool = False
    transcriber: Any = None
    executor_task: bool = True

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
            from transformers import pipeline

            values["transcriber"] = pipeline(
                "automatic-speech-recognition",
                model="openai/whisper-base.en",
            )
        except ImportError:
            raise ValueError(
                "Could not import transformers python package. "
                "Please install it with `pip install transformers`."
            )
        return values

    def transcribe(self, sr, y):
        y = y.astype(np.float32)
        y /= np.max(np.abs(y))

        return self.transcriber({"sampling_rate": sr, "raw": y})[
            "text"
        ]

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        print("input", inputs[0])
        path = self.datapipe.retrieve(inputs[0])
        sample_rate, data = wavfile.read(path)
        return self.transcribe(sample_rate, data)

    def explain(
        self,
    ) -> str:
        return "This task uses Whisper as speech to text module."
