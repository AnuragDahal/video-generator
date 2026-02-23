from pydantic import BaseModel
from typing import Optional, List

class VideoCreate(BaseModel):
    prompt: str
    aspect_ratio: str = "16:9"
    voice_provider: str = "edge-tts"

class VideoResponse(BaseModel):
    id: str
    task_id: str
    status: str
    title: Optional[str] = None
    video_url: Optional[str] = None
    script: Optional[dict] = None
    error: Optional[str] = None
