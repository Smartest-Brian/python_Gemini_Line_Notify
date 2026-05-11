from google import genai
from google.genai import types
import os

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL")
        self.client = genai.Client(api_key=self.api_key)
        self.config = types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )

    def generate_report(self, prompt):
        """
        Sends a prompt to Gemini and returns the response text.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=self.config
            )
            return response.text
        except Exception as e:
            print(f"Gemini API error: {e}")
            return f"⚠️ Gemini API Error: {str(e)}"