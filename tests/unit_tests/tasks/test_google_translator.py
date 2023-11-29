import pytest
from unittest.mock import MagicMock
from tasks.google_translator import GoogleTranslate


@pytest.fixture
def google_translate_task():
    return GoogleTranslate()


def test_google_translate_execute(google_translate_task):

    input_text = "سلام"
    destination_language = "en"

    google_translate_task._execute = MagicMock(return_value=("Hello", "fa"))

    input_args = f"{input_text}$#{destination_language}"
    result = google_translate_task.execute(input_args)

    google_translate_task._execute.assert_called_once_with([input_text, destination_language])
    assert "Hello" in result
    assert "fa" in result


def test_google_translate_parse_input(google_translate_task):

    input_args = "سلام$#en"

    result = google_translate_task._parse_input(input_args)

    assert result == ["سلام", "en"]


def test_google_translate_validate_environment():

    values = {}

    result = GoogleTranslate.validate_environment(values)

    assert "translator" in result


def test_google_translate_explain(google_translate_task):

    result = google_translate_task.explain()

    assert "This task uses google translate to translate between languages" in result
