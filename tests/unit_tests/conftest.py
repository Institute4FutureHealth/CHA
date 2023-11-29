import os
import pytest


@pytest.fixture
def get_serpapi_key():
    return os.environ.get("SERPAPI_API_KEY", "3943180048cac68ca16f1957cac660d508fa0ba36c5e362a0696734c090b3f00")


@pytest.fixture
def get_openai_key():
    return os.environ.get("OPENAI_API_KEY", "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")

