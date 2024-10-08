import pandas as pd

from src.llms.openai import OpenAILLM

kwargs = {"model_name": "gpt-4", "max_tokens": 5000}
llm = OpenAILLM()
responses = []
prefix_prompt = (
    "You are a professional nutritionist. "
    "Considering the following question, answer the user based on the risk related to Total_Carbohydrate, Total_Fat, Saturated_Fat, "
    "Protein, Sodium, Sugars, Dietary_Fiber for the whole day cumulatively. "
    "Compare the mentioned nutrients against the recommended amounts for each individual nutrients.\n"
    "Return the response in the following format:\n"
    "Total_Carbohydrate: [amount estimation in calorie %], [Risky/not Risky]. [recommended range: < 45% of energy intake]. [reason]\n"
    "Total_Fat: [amount estimation in calorie %], [Risky/not Risky]. [recommended range: 20%-35% of energy intake]. [reason]\n"
    "Saturated_Fat: [amount estimation in calorie %], [Risky/not Risky]. [recommended range: < 10% of energy intake]. [reason]\n"
    "Protein: [amount estimation in calorie %], [Risky/not Risky]. [recommended range: 15%-20% of energy intake]. [reason]\n"
    "Sodium: [amount estimation in mg], [Risky/not Risky]. [recommended range: < 2300mg]. [reason]\n"
    "Sugars: [amount estimation in g], [Risky/not Risky]. [recommended range: < 25g]. [reason]\n"
    "Dietary_Fiber: [amount estimation in g], [Risky/not Risky]. [recommended range: 20g-35g]. [reason]\n\n"
    "Question: "
)
with open("questions.txt", "r") as file:
    for line in file:
        print("prompt", prefix_prompt + line)
        responses.append(llm.generate(prefix_prompt + line, **kwargs))
        f = open("./result.txt", "a")
        f.write("\n------\n" + responses[-1] + "\n------\n")
        f.close()

df = pd.DataFrame(responses, columns=["ChatGPT Answers"])
df.to_csv("GPT4_response.csv")
