import os
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from tasks.serpapi import SerpAPI


os.environ["SERPAPI_API_KEY"] = "3943180048cac68ca16f1957cac660d508fa0ba36c5e362a0696734c090b3f00"


@pytest.fixture
def serpapi_task():
    return SerpAPI()


def test_validate_environment_with_valid_package():
    values = {"serpapi_api_key": "your_api_key_here"}
    updated_values = SerpAPI.validate_environment(values)
    assert "search_engine" in updated_values


def test_get_params(serpapi_task):
    query = "test_query"
    params = serpapi_task.get_params(query)
    assert params["api_key"] == serpapi_task.serpapi_api_key
    assert params["q"] == query


def test_results(serpapi_task):
    query = "test_query"
    expected_result = {'error': 'Invalid API key. Your API key should be here: https://serpapi.com/manage-api-key'}

    serpapi_task.search_engine = lambda params: SimpleNamespace(get_dict=lambda: expected_result)

    result = serpapi_task.results(query)
    print(result)

    assert result == expected_result


def test_process_response_with_valid_response(serpapi_task):
    valid_response = {
        "organic_results": [
            {"link": "https://example.com", "snippet": "This is a snippet."}
        ]
    }
    processed_result = serpapi_task._process_response(valid_response)
    expected_result = "url: https://example.com\nmetadata: This is a snippet."
    assert processed_result == expected_result


def test_process_response_with_invalid_response(serpapi_task):
    invalid_response = {}
    processed_result = serpapi_task._process_response(invalid_response)
    expected_result = "Could not get the proper response from the search. Try another search query."
    assert processed_result == expected_result


def test_execute(serpapi_task, mocker):
    query = "test_query"
    expected_result = {"result_key": "result_value"}
    mocker.patch.object(SerpAPI, "results", return_value=expected_result)

    result = serpapi_task._execute([query])

    assert result == serpapi_task._process_response(expected_result)


def test_explain(serpapi_task):
    explanation = serpapi_task.explain()
    assert "This task searched in the internet using google search engine" in explanation
