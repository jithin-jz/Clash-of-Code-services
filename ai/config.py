from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    # Service URLs
    CORE_SERVICE_URL: str
    
    # API Keys & Auth
    # API Keys & Auth
    INTERNAL_API_KEY: str
    GROQ_API_KEY: Optional[str] = None
    
    # LLM Settings
    LLM_PROVIDER: str = "groq" 
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    OPENAI_API_BASE: str = "https://api.groq.com/openai/v1"
    
    # RAG Settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CHROMA_SERVER_HOST: str = "chroma"
    CHROMA_SERVER_HTTP_PORT: int = 8000
    
    # Security
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("CORS_ORIGINS", mode="before")
    def split_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    def validate_keys(self):
        if not self.GROQ_API_KEY:
            raise ValueError("Missing LLM API Key: GROQ_API_KEY must be set")

settings = Settings()
settings.validate_keys()

