from pydantic import BaseModel
from typing import Optional, List

class VideoCreate(BaseModel):
    prompt: str
    aspect_ratio: str = "16:9"
    voice_provider: str = "edge-tts"

class VideoResponse(BaseModel):
    id: str
    status: str
    video_url: Optional[str] = None
    script: Optional[str] = None
    error: Optional[str] = None
