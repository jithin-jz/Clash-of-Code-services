import logging
from typing import Optional
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import HTTPException
from config import settings

logger = logging.getLogger(__name__)

class LLMFactory:
    @staticmethod
    def get_llm(provider: Optional[str] = None) -> BaseChatModel:
        """
        Returns a configured LLM instance based on the provider.
        Defaults to settings.LLM_PROVIDER if not specified.
        """
        provider = provider or settings.LLM_PROVIDER
        
        if provider == "groq":
            if not settings.GROQ_API_KEY:
                logger.warning("Groq API Key missing, attempting fallback to Gemini")
                return LLMFactory.get_llm("gemini")
                
            logger.info("Initializing Groq LLM (via OpenAI compatible API)")
            return ChatOpenAI(
                api_key=settings.GROQ_API_KEY,
                base_url=settings.OPENAI_API_BASE,
                model=settings.MODEL_NAME, # 'llama-3.3-70b-versatile' typically
                temperature=0.7
            )
            
        elif provider == "gemini":
            if not settings.GEMINI_API_KEY:
                raise ValueError("Gemini API Key missing")
                
            logger.info("Initializing Gemini LLM")
            return ChatGoogleGenerativeAI(
                google_api_key=settings.GEMINI_API_KEY,
                model="gemini-1.5-flash", # Explicitly use a Gemini model name
                temperature=0.7
            )
            
        else:
             # Default fallback - try Groq first, then Gemini
             logger.warning(f"Unknown provider '{provider}', falling back to auto-selection")
             if settings.GROQ_API_KEY: return LLMFactory.get_llm("groq")
             if settings.GEMINI_API_KEY: return LLMFactory.get_llm("gemini")
             
             raise ValueError("No valid LLM configuration found")

    @staticmethod
    def get_fallback_llm() -> BaseChatModel:
        """
        Returns the secondary/fallback LLM (usually Gemini).
        """
        if settings.GEMINI_API_KEY:
            return LLMFactory.get_llm("gemini")
        elif settings.GROQ_API_KEY:
             return LLMFactory.get_llm("groq")
        else:
            raise ValueError("No LLM keys available for fallback")
