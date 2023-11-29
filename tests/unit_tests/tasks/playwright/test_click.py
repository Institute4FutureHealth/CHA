from unittest.mock import MagicMock, patch, Mock

import pytest
from playwright.sync_api import sync_playwright

from tasks.playwright import Click


@pytest.fixture
def click_task():
    
    return Click()


def test_click_success(click_task, mocker):
    
    mocker.patch('tasks.playwright.click.get_current_page')
    mocker.patch('tasks.playwright.click.PlaywrightTimeoutError')

    click_task.visible_only = True

    result = click_task._execute(["your_css_selector"])

    assert result == "Clicked element 'your_css_selector'"


def test_click_failure(click_task):
    result = click_task._execute(["non_existing_selector"])
    assert "Unable to click on element 'non_existing_selector'" in result

