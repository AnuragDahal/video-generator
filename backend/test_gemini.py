from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

try:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents="Provide me a youtube video script for a video topic on 'The mystery of the Bermuda Triangle'.",
        config=types.GenerateContentConfig(
            system_instruction="You are a professional video script writer. Generate a concise and engaging script based on the user's prompt.You will return the response in plain text not in a markdown syntax."
        )
    )

    print("SUCCESS:")
    print(response.text)
except Exception as e:
    print("FAILED:")
    print(e)
