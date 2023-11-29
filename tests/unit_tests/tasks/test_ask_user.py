import pytest
from unittest.mock import MagicMock
from tasks.ask_user import AskUser


def test_ask_user_execute():
    user_input = "User input text."
    ask_user_task = AskUser()

    ask_user_task._execute = MagicMock(return_value=user_input)

    result = ask_user_task.execute(user_input)

    assert result == user_input
    ask_user_task._execute.assert_called_once_with([user_input])

