import pytest

from tasks.nutritionix import QueryNutritionix


def test_query_nutritionix_execute():
    query = "Every morning, I starts my day with a cheeseburger, a bottle of milk, and two eggs for breakfast."

    query_nutritionix_task = QueryNutritionix()

    result = query_nutritionix_task._execute([query])
    print(result)
    assert isinstance(result, str)
