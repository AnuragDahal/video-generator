from google import genai
from google.genai import types
import json
import re
from app.core.config import settings

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

        system_instruction = (
            "You are a professional YouTube script writer and director. "
            "Your goal is to create a highly engaging video script including narration and visual cues. "
            "You MUST return the response as a JSON object with the following structure:\n"
            "{\n"
            "  \"title\": \"Direct and catchy title\",\n"
            "  \"narration\": \"The full, continuous narration text without any scene markers or instructions. This will be read by an AI voice.\",\n"
            "  \"scenes\": [\n"
            "    {\n"
            "      \"narration_part\": \"The specific part of the narration for this scene\",\n"
            "      \"visual_keywords\": [\"keyword1\", \"keyword2\", \"keyword3\"]\n"
            "    }\n"
            "  ]\n"
            "}\n"
            "Ensure you provide at least 5-8 scenes to keep the video visually dynamic. "
            "Keywords should be descriptive for high-quality stock image searches (e.g., 'crashing ocean waves', 'vintage 1940s airplane')."
        )

        try:
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    thinking_config=types.ThinkingConfig(thinking_level='low')
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
