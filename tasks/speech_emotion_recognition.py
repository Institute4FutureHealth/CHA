from typing import Any
from typing import Dict
from typing import List

from pydantic import model_validator

from tasks.task import BaseTask


class SpeechEmotionRecognition(BaseTask):
    """
    **Description:**

        This task is converts user audio into text to start planning and answering.

    """

    name: str = "speech_emotion_recognition"
    chat_name: str = "SpeechEmotionRecognition"
    description: str = (
        "This task converts audio into text. It support wav and mp3 file extention. "
        "You should use this task only if inside the Meta Data there are some audio files with .wav suffix."
    )
    dependencies: List[str] = []
    inputs: List[str] = ["The meta data id of the audio path."]
    outputs: List[str] = [
        "It returns the emotion state in following format: "
        "**The emotion detected for the audio file: [filename] is [one of the four emotions: Happy, Angry, Neutral, Sad]}**"
    ]
    return_direct: bool = False
    classifier: Any = None

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
            from speechbrain.inference.interfaces import foreign_class

            values["classifier"] = foreign_class
        except ImportError:
            raise ValueError(
                "Could not import transformers python package. "
                "Please install it with `pip install transformers`."
            )
        return values

    def get_emotion(self, emotion):
        if emotion[0] == "ang":
            return "Angry"
        if emotion[0] == "hap":
            return "Happy"
        if emotion[0] == "neu":
            return "Neutral"
        if emotion[0] == "sad":
            return "Sad"

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        classifier = self.classifier(
            source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
            pymodule_file="custom_interface.py",
            classname="CustomEncoderWav2vec2Classifier",
        )
        out_prob, score, index, text_lab = classifier.classify_file(
            inputs[0]["path"]
        )
        return f"The emotion detected for the audio file: {inputs[0]['path'].split('/')[-1]} is {self.get_emotion(text_lab)}"

    def explain(
        self,
    ) -> str:
        return "This task uses Whisper as speech to text module."
