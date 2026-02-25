from google import genai
from google.genai import types
import json
import re
from app.core.config import settings
from app.utils.prompts import script_prompt


class ScriptService:
    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None

    async def generate_script(self, prompt: str) -> dict:
        """
        Generates a structured script including narration and visual keywords.
        Returns a dictionary with 'narration' and 'scenes'.
        """
        if not self.client:
            if settings.GEMINI_API_KEY:
                self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            else:
                return {"error": "GEMINI_API_KEY not configured."}

        system_instruction = script_prompt

        try:
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    # thinking_config=types.ThinkingConfig(thinking_level='low')
                ),
                contents=prompt
            )

            # Extract JSON from response
            script_data = json.loads(response.text)
            return script_data

        except Exception as e:
            print(f"Error in script generation: {e}")
            return {"error": str(e)}


script_service = ScriptService()
