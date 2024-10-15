import time

import pandas as pd
from tasks import initialize_task
from tasks import TaskType

query_nutritionix = initialize_task(task=TaskType.QUERY_NUTRITIONIX)
calculate_food_risk_factor = initialize_task(
    task=TaskType.CALCULATE_FOOD_RISK_FACTOR
)
responses = []

with open("questions.txt", "r") as file:
    for line in file:
        print(line)
        foods = query_nutritionix._execute([line])
        responses.append(
            calculate_food_risk_factor._execute([{"data": foods}])
        )
        f = open("./baseline_result.txt", "a")
        f.write("\n------\n" + responses[-1] + "\n------\n")
        f.close()
        time.sleep(3)


df = pd.DataFrame(responses, columns=["Baseline Answers"])
df.to_csv("baseline_response.csv")
