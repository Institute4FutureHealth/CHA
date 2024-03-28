import pytest

from tasks.audio_to_text import AudioToText


def test_ask_user_execute():
    input = "tests/unit_tests/test_data/audio.wav"
    audio_to_text = AudioToText()

    result = audio_to_text._execute([{"path": input}])
    print(result)
    assert result == " you"
