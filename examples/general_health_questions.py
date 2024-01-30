from src.CHA import CHA
from src.tasks.playwright.utils import create_sync_playwright_browser

sync_browser = create_sync_playwright_browser()
available_tasks = ["serpapi", "extract_text", "ask_user"]
chat_history = []

while True:
    user_query = input("Ask your question: ")
    cha = CHA(sync_browser=sync_browser)
    response = cha.run(
        user_query,
        chat_history=chat_history,
        available_tasks=available_tasks,
        use_history=True,
    )
    print("CHA: ", response)

    chat_history.append((user_query, response))
