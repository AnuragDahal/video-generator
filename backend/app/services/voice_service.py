from app.core.config import settings

class VoiceService:
    @staticmethod
    async def generate_voiceover(script: str, output_path: str, provider: str = "edge-tts") -> str:
        """
        Generates audio file from script using ElevenLabs or Edge TTS.
        """
        # Placeholder for implementation
        return output_path

voice_service = VoiceService()
