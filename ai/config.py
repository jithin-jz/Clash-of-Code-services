import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Service URLs
    CORE_SERVICE_URL = os.getenv("CORE_SERVICE_URL")
    PISTON_URL = os.getenv("PISTON_URL")
    
    # API Keys & Auth
    INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # LLM Settings
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq") # groq, gemini
    MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.groq.com/openai/v1")
    
    # RAG Settings
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma_db")
    
    # Security
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost").split(",")

    @classmethod
    def validate(cls):
        missing = []
        if not cls.CORE_SERVICE_URL: missing.append("CORE_SERVICE_URL")
        if not cls.PISTON_URL: missing.append("PISTON_URL")
        if not cls.INTERNAL_API_KEY: missing.append("INTERNAL_API_KEY")
        
        # Require at least one LLM provider
        if not cls.GEMINI_API_KEY and not cls.GROQ_API_KEY:
            missing.append("LLM API Key (GEMINI_API_KEY or GROQ_API_KEY)")
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

settings = Config()
settings.validate()

