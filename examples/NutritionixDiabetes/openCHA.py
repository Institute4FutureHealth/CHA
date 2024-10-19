import pandas as pd
from CHA import CHA
from tasks import TaskType

available_tasks = [
    TaskType.QUERY_NUTRITIONIX,
    TaskType.CALCULATE_FOOD_RISK_FACTOR,
]
responses = []

response_generator_prefix_prompt = (
    "You are a professional nutritionist. "
    "Return the response in the following format:\n"
    "Total_Carbohydrate: [amount estimation in calorie %], [Risky/not Risky]. [recommended range: < 45% of energy intake]. [reason]\n"
    "Total_Fat: [amount estimation in calorie %], [Risky/not Risky]. [recommended range: 20%-35% of energy intake]. [reason]\n"
    "Saturated_Fat: [amount estimation in calorie %], [Risky/not Risky]. [recommended range: < 10% of energy intake]. [reason]\n"
    "Protein: [amount estimation in calorie %], [Risky/not Risky]. [recommended range: 15%-20% of energy intake]. [reason]\n"
    "Sodium: [amount estimation in mg], [Risky/not Risky]. [recommended range: < 2300mg]. [reason]\n"
    "Sugars: [amount estimation in g], [Risky/not Risky]. [recommended range: < 25g]. [reason]\n"
    "Dietary_Fiber: [amount estimation in g], [Risky/not Risky]. [recommended range: 20g-35g]. [reason]\n\n"
    "\n\nQuestion: "
)

planner_prefix = (
    "Based on the question, always query nutritionix and provide the whole day food. Do not decompose the food. "
    "Then calculate food risk factor."
)

kwargs = {
    "response_generator_prefix_prompt": response_generator_prefix_prompt
}

with open("questions.txt", "r") as file:
    for line in file:
        cha = CHA()
        responses.append(
            cha.run(
                planner_prefix + line,
                available_tasks=available_tasks,
                **kwargs
            )
        )
        f = open("./result_openCHA.txt", "a")
        f.write("\n------\n" + responses[-1] + "\n------\n")
        f.close()

df = pd.DataFrame(responses, columns=["openCHA Answers"])
df.to_csv("openCHA_response.csv")
