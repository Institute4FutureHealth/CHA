from typing import Any
from typing import Dict
from typing import List

import requests
from openCHA.tasks import BaseTask
from openCHA.utils import get_from_dict_or_env
from pydantic import model_validator


class QueryNutritionix(BaseTask):
    """
    **Description:**

        This task queries the nutrition contents from nutritionix of a meal or multiple meals and returns the details nutritions values.

    """

    name: str = "query_nutritionix"
    chat_name: str = "Nutritionix"
    description: str = "Queries the nutrition contents of a meal or multiple meals and returns the details nutritions values."
    dependencies: List[str] = []
    inputs: List[str] = [
        "The query that contains the daily foods, their portion, restaurant and other information regarding the food. You can query all together"
        "A query example is: "
        "**Every morning, I starts my day with a cheeseburger, a bottle of milk, and two eggs for breakfast.** "
        "or **cheeseburger, bottle, milk, 2 eggs**"
        "This tool will calculate all the foods all at once. no need to separately query them."
    ]
    outputs: List[str] = [
        "Returns a JSON object containing **foods** key. The **foods** is an array of the food objects with the following information: "
        "**food_name**: The name of the food.\n"
        "**brand_name**: The name of the brand of the food.\n"
        "**serving_qty**: The serving quantity of the food.\n"
        "**serving_unit**: The serving unit of the food.\n"
        "**serving_weight_grams**: The weight of serving size of the food.\n"
        "**nf_calories**: The calories of the food for the serving size.\n"
        "**nf_total_fat**: The total fat of the food for the serving size.\n"
        "**nf_saturated_fat**: The total saturated fat of the food for the serving size.\n"
        "**nf_cholesterol**: The total cholesterol of the food for the serving size.\n"
        "**nf_sodium**: The total sodium of the food for the serving size.\n"
        "**nf_total_carbohydrate**: The total carbohydrate of the food for the serving size.\n"
        "**nf_dietary_fiber**: The total dietary fiber of the food for the serving size.\n"
        "**nf_sugars**: The total sugars of the food for the serving size.\n"
        "**nf_protein**: The total protein of the food for the serving size.\n"
        "**nf_potassium**: The total potassium of the food for the serving size.\n"
        "**nf_p**: The total phosphorus of the food for the serving size.\n"
        "**full_nutrients**: The detailed list of the nutrients.\n"
    ]
    output_type: bool = True

    url: str = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers: object = {}

    @model_validator(mode="before")
    def validate_environment(cls, values: Dict) -> Dict:
        """
            Validate that api key and python package exists in environment.

        Args:
            values (Dict): The dictionary of attribute values.
        Return:
            Dict: The updated dictionary of attribute values.
        Raise:
            ValueError: If the SerpAPI python package is not installed.

        """

        nutritionix_api_key = get_from_dict_or_env(
            values, "nutritionix_api_key", "NUTRITIONIX_API_KEY"
        )

        nutritionix_app_id = get_from_dict_or_env(
            values, "nutritionix_app_id", "NUTRITIONIX_APP_ID"
        )

        if nutritionix_api_key is None:
            raise ValueError(
                "The nutritionx_api_key or NUTRITIONIX_API_KEY is not provided!"
            )
        if nutritionix_app_id is None:
            raise ValueError(
                "The nutritionix_app_id or NUTRITIONIX_APP_ID is not provided!"
            )

        values["headers"] = {
            "Content-Type": "application/json",
            "x-app-id": nutritionix_app_id,
            "x-app-key": nutritionix_api_key,
        }
        return values

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        query = inputs[0]
        body = {"query": query}
        response = requests.post(
            self.url, json=body, headers=self.headers
        )

        foods = response.json()
        return foods

    def explain(
        self,
    ) -> str:
        return "This task simply asks user to provide more information or continue interaction."
