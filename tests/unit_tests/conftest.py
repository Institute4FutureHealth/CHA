import os

import pytest


@pytest.fixture
def get_serpapi_key():
    return os.environ.get("SERPAPI_API_KEY")


@pytest.fixture
def get_openai_key():
    return os.environ.get("OPENAI_API_KEY")
