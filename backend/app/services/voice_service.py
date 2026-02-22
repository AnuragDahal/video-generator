import edge_tts
import asyncio
import os
import re
from pathlib import Path
from elevenlabs.client import ElevenLabs
from app.core.config import settings

class VoiceService:
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.client = ElevenLabs(api_key=self.api_key) if self.api_key else None
        self.output_dir = Path(settings.OUTPUT_DIR) / "audio"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_voiceover(self, script: str, output_filename: str = "voiceover.mp3") -> str:
        """
        Generates audio file from script.
        Tries ElevenLabs first, falls back to Edge TTS if ElevenLabs fails or is blocked.
        """
        output_path = self.output_dir / output_filename

        # 1. Try ElevenLabs if API key is present
        if self.client:
            try:
                print(f"Attempting ElevenLabs generation for: {output_filename}")
                # Use correct model_id and voice_id
                # model_id is required in the latest SDK for .convert()
                audio = self.client.text_to_speech.convert(
                    text=script,
                    voice_id="JBFqnCBsd6RMkjVDRZzb", # Adam
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128"
                )
                
                with open(output_path, "wb") as f:
                    for chunk in audio:
                        if chunk:
                            f.write(chunk)
                
                print(f"ElevenLabs voiceover generated: {output_path}")
                return str(output_path)
            except Exception as e:
                print(f"ElevenLabs failed or blocked: {e}")
                print("Falling back to Edge TTS...")

        # 2. Fallback to Edge TTS (Free, no API key required)
        try:
            print(f"Attempting Edge TTS generation for: {output_filename}")
            # 'en-US-ChristopherNeural' is a good high-quality male voice
            communicate = edge_tts.Communicate(script, "en-US-ChristopherNeural")
            await communicate.save(output_path)
            
            print(f"Edge TTS voiceover generated: {output_path}")
            return str(output_path)
        except Exception as e:
            error_msg = f"Both ElevenLabs and Edge TTS failed: {e}"
            print(error_msg)
            return f"Error: {error_msg}"

voice_service = VoiceService()
