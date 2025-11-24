from ai_brain import ask_ai
from ai_image import create_image

history = []

def main():
    while True:
        user_input = input("\nYou: ")

        if user_input.startswith("!img "):
            prompt = user_input[5:]
            create_image(prompt)
            continue

        bot_reply = ask_ai(user_input, history)

        print("\nAI:", bot_reply)

        history.append((user_input, bot_reply))

if __name__ == "__main__":
    main()
