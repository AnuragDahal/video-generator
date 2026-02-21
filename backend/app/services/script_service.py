from app.core.config import settings

class ScriptService:
    @staticmethod
    async def generate_script(prompt: str, provider: str = "gemini") -> str:
        """
        Generates a script based on the prompt using specified AI provider.
        """
        # Placeholder for implementation
        # Will use Gemini, Groq, or Grok free tier
        return f"This is a generated script for: {prompt}"

script_service = ScriptService()
