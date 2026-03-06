from chatbot import chat, create_chat_history, MAX_TURNS

chat_history = create_chat_history()


def main():
    print("LangChain Chatbot Ready! (Type 'quit' to exit, 'clear' to reset history)")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "quit":
            break

        if user_input.lower() == "clear":
            chat_history.clear()
            print("History Cleared.")
            continue

        response, chat_history = chat(user_input, chat_history)
        print("AI:", response)


if __name__ == "__main__":
    main()
