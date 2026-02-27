from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Video Generator API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # AI Service Keys
    GEMINI_API_KEY: str
    GEMINI_MODEL: str
    
    # Audio Services
    ELEVENLABS_API_KEY: str
    
    # Visual Services
    PEXELS_API_KEY: str
    
    # Storage & Cloud
    OUTPUT_DIR: str = "outputs"
    SUPABASE_URL: Optional[str] = None
    SUPABASE_ANON_PUBLIC_KEY: Optional[str] = None
    SUPABASE_BUCKET: str = "videos"

    # Redis for Celery and PubSub
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()

