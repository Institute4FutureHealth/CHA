import pytest

from tasks import GoogleSearch


def test_query_nutritionix_execute():
    query = "How to improve my sleep?"

    google_search = GoogleSearch()

    result = google_search._execute([query])
    print(result)
    assert isinstance(result, dict)
