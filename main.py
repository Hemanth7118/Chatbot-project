import os
from dotenv import load_dotenv
from google import genai

# 1. Load the secret API key
load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    print("Error: API_KEY not found. Please check your .env file.")
    exit(1)

# 2. Configure the AI provider
client = genai.Client(api_key=api_key)

# 3. Start a chat session (this automatically handles conversation history)
chat = client.chats.create(model='gemini-flash-latest')

print("Bot is ready! (Type 'quit' to exit)")
print("-" * 30)

# 4. Create the chat loop
while True:
    try:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ['quit', 'exit']:
            print("Bot: Goodbye!")
            break

        # Send the message to the AI
        response = chat.send_message(user_input)
        print(f"Bot: {response.text}\n")
    except KeyboardInterrupt:
        print("\nBot: Session ended by user. Goodbye!")
        break
    except Exception as e:
        print(f"An error occurred: {e}")

'''models = client.models.list()
for model in models:
    print(model.name)'''