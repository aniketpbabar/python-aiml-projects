import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
SYSTEM = "You are a helpful assistant for data engineers. Keep answers short."

# the chat history
history = []
def ask(user_message):
    history.append({"role": "user", "content": user_message})
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=500,
        system=SYSTEM,
        messages=history,
    )
    answer = response.content[0].text
    history.append({"role": "assistant", "content": answer})
    return answer

print("Chatbot ready. Type 'quit' to exit.")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ("quit", "exit"):
        print("Bye-bye.")
        break
    print(f"\nBot: {ask(user_input)}")
