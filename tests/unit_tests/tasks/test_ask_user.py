import pytest

from tasks.internals.ask_user import AskUser


def test_ask_user_execute():
    user_input = "User input text."
    ask_user_task = AskUser()

    result = ask_user_task._execute([user_input])

    assert result == user_input
