# config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Mem0.ai settings
    MEM0_API_KEY: str
    MEM0_API_URL: str = "https://api.mem0.ai/v1"
    
    # Database settings (if needed later)
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # API settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "AI Tutor"
    
    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()