import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def get_player_stats(player_name: str) -> str:
    return f"Stats for {player_name}"

client = genai.Client(api_key=api_key)

config = types.GenerateContentConfig(
    system_instruction="You are a helpful assistant.",
    tools=[get_player_stats],
)

chat = client.chats.create(model="gemini-2.0-flash", config=config)

try:
    response = chat.send_message("What are the stats for Virat Kohli?")
    print("SUCCESS! Response:", response.text)
except Exception as e:
    print("FAILED!", str(e))
