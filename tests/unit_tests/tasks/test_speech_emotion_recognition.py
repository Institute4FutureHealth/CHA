import pytest

from tasks.speech_emotion_recognition import SpeechEmotionRecognition


def test_speech_emotion_rec_execute():
    speech_emotion_recognition = SpeechEmotionRecognition()
    input = "tests/unit_tests/test_data/amused_1-15_0001.wav"

    result = speech_emotion_recognition._execute([{"path": input}])
    print(result)
    assert (
        f"The emotion detected for the audio file: {input.split('/')[-1]} is Happy"
        == result
    )
