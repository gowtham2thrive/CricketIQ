import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

try:
    response = model.generate_content("Hello, this is a test. Are you there?")
    print("SUCCESS! The API responded:")
    print(response.text)
except Exception as e:
    print(f"FAILED! Error details:\n{str(e)}")
