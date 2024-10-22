from openCHA import openCHA

available_tasks = ["serpapi", "extract_text", "ask_user"]
chat_history = []

while True:
    user_query = input("Ask your question: ")
    cha = openCHA()
    response = cha.run(
        user_query,
        chat_history=chat_history,
        available_tasks=available_tasks,
        use_history=True,
    )
    print("CHA: ", response)

    chat_history.append((user_query, response))
