import json
from typing import Any
from typing import List

import pandas as pd
import requests
from pydantic import model_validator

from tasks.task import BaseTask


class CalculateFoodRiskFactor(BaseTask):
    """
    **Description:**

            This task is asking question back to the user and stops planning. When needed, the planner will decide to ask question from user
            and use the user's answer to proceed to the planning.

    """

    name: str = "calculate_food_risk_factor"
    chat_name: str = "CalculateFoodRiskFactor"
    description: str = "Calculates the daily foods risk factor for diabetes using evidence based nutritional method."
    dependencies: List[str] = []
    inputs: List[str] = [
        "The Nutritional value of the foods for the whole day in form of a datapipe."
    ]
    outputs: List[str] = [
        "Returns a JSON object containing the total value as well as risk factor:"
        "**Calories**: The calories of the food for the serving size.\n"
        "**Calories_Risk**: The risk of the total consumed calories based on the guidelines.\n"
        "**Total_Fat**: The total fat of the food for the serving size.\n"
        "**Total_Fat_Risk**: The risk of the total consumed fat based on the guidelines.\n"
        "**Saturated_Fat**: The total saturated fat of the food for the serving size.\n"
        "**Saturated_Fat_Risk**: The risk of the total consumed saturated fat based on the guidelines.\n"
        "**Cholesterol**: The total cholesterol of the food for the serving size.\n"
        "**Cholesterol_Risk**: The risk of the total consumed cholesterol based on the guidelines.\n"
        "**Sodium**: The total sodium of the food for the serving size.\n"
        "**Sodium_Risk**: The risk of the total consumed sodium based on the guidelines.\n"
        "**Total_Carbohydrate**: The total carbohydrate of the food for the serving size.\n"
        "**Total_Carbohydrate_Risk**: The risk of the total consumed carbohydrate based on the guidelines.\n"
        "**Dietary_Fiber**: The total dietary fiber of the food for the serving size.\n"
        "**Dietary_Fiber_Risk**: The risk of the total consumed fiber based on the guidelines.\n"
        "**Sugars**: The total sugars of the food for the serving size.\n"
        "**Sugars_Risk**: The risk of the total consumed sugars based on the guidelines.\n"
        "**Protein**: The total protein of the food for the serving size.\n"
        "**Protein_Risk**: The risk of the total consumed protein based on the guidelines.\n"
        "**Potassium**: The total potassium of the food for the serving size.\n"
        "**Potassium_Risk**: The risk of the total consumed potassium based on the guidelines.\n"
        "**Phosphorus**: The total phosphorus of the food for the serving size.\n"
        "**Phosphorus_Risk**: The risk of the total consumed phosphorus based on the guidelines.\n"
    ]
    output_type: bool = True

    def check_rules(self, total_intake):
        fat_calorie_ratio = 9
        saturated_fat_calorie_ratio = 9
        protein_calorie_ratio = 4
        carbohydrates_calorie_ratio = 4

        carb = (
            total_intake["Total_Carbohydrate"]
            * carbohydrates_calorie_ratio
        ) / total_intake["Calories"]
        fat = (
            total_intake["Total_Fat"] * fat_calorie_ratio
        ) / total_intake["Calories"]
        saturated_fat = (
            total_intake["Saturated_Fat"]
            * saturated_fat_calorie_ratio
        ) / total_intake["Calories"]
        protein = (
            total_intake["Protein"] * protein_calorie_ratio
        ) / total_intake["Calories"]

        is_carb_risk = carb > 0.45
        is_fat_risk = fat < 0.2 or fat > 0.35
        is_saturated_fat_risk = saturated_fat > 0.1
        is_protein_risk = protein < 0.15 or protein > 0.2
        is_sodium_risk = total_intake["Sodium"] > 2300
        is_sugars_risk = total_intake["Sugars"] > 25
        is_fiber_risk = (
            total_intake["Dietary_Fiber"] < 20
            or total_intake["Dietary_Fiber"] > 35
        )

        return {
            "Total_Carbohydrate_Risk": "No Risk"
            if not is_carb_risk
            else f"The percentage of total carnohydrate of total energy intake is {int(carb*100)}% "
            "which exceeds the recommended threshold of < 45%",
            "Total_Fat_Risk": "No Risk"
            if not is_fat_risk
            else f"The percentage of total fat of total energy intake is {int(fat*100)}% "
            "which is outside the recommended threshold of 20%-35%",
            "Saturated_Fat_Risk": "No Risk"
            if not is_saturated_fat_risk
            else f"The percentage of total saturated fat of total energy intake is {int(saturated_fat*100)}% "
            "which exceeds the recommended threshold of < 10%",
            "Protein_Risk": "No Risk"
            if not is_protein_risk
            else f"The percentage of total protein of total energy intake is {int(saturated_fat*100)}% "
            "which is outside the recommended threshold of 15%-20%",
            "Sodium_Risk": "No Risk"
            if not is_sodium_risk
            else f"The total consumed sodium is {total_intake['Sodium']}mg "
            "which is more than recommended threshold of 2300mg",
            "Sugars_Risk": "No Risk"
            if not is_sugars_risk
            else f"The total consumed sugar is {total_intake['Sugars']}g "
            "which is more than recommended threshold of 25g",
            "Dietary_Fiber_Risk": "No Risk"
            if not is_fiber_risk
            else f"The total consumed fiber is {total_intake['Dietary_Fiber']}g "
            "which is outside the recommended values of 20g-35g",
        }

    def process_nutrients(self, nutrition_json):
        total_nutrients = {
            "Calories": 0,
            "Total_Fat": 0,
            "Saturated_Fat": 0,
            "Cholesterol": 0,
            "Sodium": 0,
            "Total_Carbohydrate": 0,
            "Dietary_Fiber": 0,
            "Sugars": 0,
            "Protein": 0,
            "Potassium": 0,
            "Phosphorus": 0,
        }

        for food in nutrition_json["foods"]:
            total_nutrients["Calories"] += (
                food["nf_calories"]
                if ("nf_calories" in food)
                and (food["nf_calories"] is not None)
                else 0
            )
            total_nutrients["Total_Fat"] += (
                food["nf_total_fat"]
                if ("nf_total_fat" in food)
                and (food["nf_total_fat"] is not None)
                else 0
            )
            total_nutrients["Saturated_Fat"] += (
                food["nf_saturated_fat"]
                if ("nf_saturated_fat" in food)
                and (food["nf_saturated_fat"] is not None)
                else 0
            )
            total_nutrients["Cholesterol"] += (
                food["nf_cholesterol"]
                if ("nf_cholesterol" in food)
                and (food["nf_cholesterol"] is not None)
                else 0
            )
            total_nutrients["Sodium"] += (
                food["nf_sodium"]
                if ("nf_sodium" in food)
                and (food["nf_sodium"] is not None)
                else 0
            )
            total_nutrients["Total_Carbohydrate"] += (
                food["nf_total_carbohydrate"]
                if ("nf_total_carbohydrate" in food)
                and (food["nf_total_carbohydrate"] is not None)
                else 0
            )
            total_nutrients["Dietary_Fiber"] += (
                food["nf_dietary_fiber"]
                if ("nf_dietary_fiber" in food)
                and (food["nf_dietary_fiber"] is not None)
                else 0
            )
            total_nutrients["Sugars"] += (
                food["nf_sugars"]
                if ("nf_sugars" in food)
                and (food["nf_sugars"] is not None)
                else 0
            )
            total_nutrients["Protein"] += (
                food["nf_protein"]
                if ("nf_protein" in food)
                and (food["nf_protein"] is not None)
                else 0
            )
            total_nutrients["Potassium"] += (
                food["nf_potassium"]
                if ("nf_potassium" in food)
                and (food["nf_potassium"] is not None)
                else 0
            )
            total_nutrients["Phosphorus"] += (
                food["nf_p"]
                if ("nf_p" in food) and (food["nf_p"] is not None)
                else 0
            )

        risks = self.check_rules(total_nutrients)

        total_nutrients[
            "Total_Fat"
        ] = f'{total_nutrients["Total_Fat"]}g'
        total_nutrients[
            "Saturated_Fat"
        ] = f'{total_nutrients["Saturated_Fat"]}g'
        total_nutrients[
            "Cholesterol"
        ] = f'{total_nutrients["Cholesterol"]}mg'
        total_nutrients["Sodium"] = f'{total_nutrients["Sodium"]}mg'
        total_nutrients[
            "Total_Carbohydrate"
        ] = f'{total_nutrients["Total_Carbohydrate"]}g'
        total_nutrients[
            "Dietary_Fiber"
        ] = f'{total_nutrients["Dietary_Fiber"]}g'
        total_nutrients["Sugars"] = f'{total_nutrients["Sugars"]}g'
        total_nutrients["Protein"] = f'{total_nutrients["Protein"]}g'
        total_nutrients[
            "Potassium"
        ] = f'{total_nutrients["Potassium"]}mg'
        total_nutrients[
            "Phosphorus"
        ] = f'{total_nutrients["Phosphorus"]}mg'

        return {**total_nutrients, **risks}

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        nutrients = inputs[0]["data"]
        result = self.process_nutrients(nutrients)
        return json.dumps(result)

    def explain(
        self,
    ) -> str:
        return "This task simply asks user to provide more information or continue interaction."
