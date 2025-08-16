import agent
print("main")
if __name__ == "__main__":
    while True:
        user_input = input("Me: ")
        if user_input.lower() == "stop":
            break
        print("Me: ", user_input)
        print("Bot:", agent.chat_with_agent(user_input))
