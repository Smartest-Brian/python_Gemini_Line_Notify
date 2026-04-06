from google import genai
import os
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

# List all available models
for model in client.models.list():
    print(f"Model Name: {model.name}")
