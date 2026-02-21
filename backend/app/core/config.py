from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Video Generator API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # AI Service Keys
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    GROK_API_KEY: Optional[str] = None
    
    # Audio Services
    ELEVENLABS_API_KEY: Optional[str] = None
    
    # Visual Services
    PEXELS_API_KEY: Optional[str] = None
    
    # Storage
    OUTPUT_DIR: str = "outputs"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
