from google import genai
from google.genai import types
from app.core.config import settings


class ScriptService:
    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None

    async def generate_script(self, prompt: str, provider: str = "gemini") -> str:
        """
        Generates a script based on the prompt using specified AI provider.
        """
        if not self.client:
            # Fallback or initialization if key wasn't available at startup
            if settings.GEMINI_API_KEY:
                self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            else:
                return "Error: GEMINI_API_KEY not configured."

        try:
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                config=types.GenerateContentConfig(
                    system_instruction="You are a professional video script writer. Generate a concise and engaging script based on the user's prompt.",
                    thinking_config=types.ThinkingConfig(thinking_level='low')
                ),
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error generating script: {str(e)}"


script_service = ScriptService()
