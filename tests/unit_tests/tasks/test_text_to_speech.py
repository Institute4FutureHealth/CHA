import pytest

from tasks.text_to_speech import TextToSpeech


def test_ask_user_execute():
    text_to_speech = TextToSpeech()

    result = text_to_speech._execute(
        ["Hi, How are you. I hope you are doing well.", "en"]
    )
    print(result)
    assert "mp3" in result
