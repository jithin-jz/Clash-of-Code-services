import os
import sys
import logging
from typing import Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import requests

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Local imports
from config import settings
# Lazy imports for big_bang and auto_generator to avoid potential circular/init issues if any
from big_bang import run_big_bang

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ChromaDB workaround for some systems
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

load_dotenv()

# Initialize App
app = FastAPI(
    title="AI Service",
    version="1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Components
# Using local embedding model to save API costs
embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
vector_db = Chroma(persist_directory=settings.CHROMA_PATH, embedding_function=embeddings)

# --- Models ---
class HintRequest(BaseModel):
    user_code: str
    challenge_slug: str
    language: str = "python"
    hint_level: int = 1  # 1: Vague, 2: Moderate, 3: Specific
    user_xp: int = 0

# --- Routes ---

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/big-bang")
async def trigger_big_bang(
    background_tasks: BackgroundTasks, 
    levels: int = 5, 
    x_internal_api_key: Optional[str] = Header(None, alias="X-Internal-API-Key")
):
    """
    Triggers the autonomous curriculum generation in the background.
    """
    if x_internal_api_key != settings.INTERNAL_API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
        
    background_tasks.add_task(run_big_bang, levels)
    return {"message": f"Big Bang started for {levels} levels. Check AI logs for progress."}

@app.post("/generate-level")
async def generate_single_level(
    background_tasks: BackgroundTasks, 
    level: int, 
    user_id: Optional[int] = None, 
    x_internal_api_key: Optional[str] = Header(None, alias="X-Internal-API-Key")
):
    """
    Generates a specific single level in the background.
    """
    if x_internal_api_key != settings.INTERNAL_API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")

    def _run_single(lvl, uid):
        from auto_generator import AutoGenerator
        
        logger.info(f"Generating Single Level {lvl} for User {uid}...")
        try:
            generator = AutoGenerator()
            challenge_json = generator.generate_level(lvl, user_id=uid)
            
            headers = {
                "X-Internal-API-Key": settings.INTERNAL_API_KEY,
                "Content-Type": "application/json"
            }
            url = f"{settings.CORE_SERVICE_URL}/api/challenges/"
            challenge_json["order"] = lvl
            if uid:
                challenge_json["created_for_user_id"] = uid
            
            response = requests.post(url, json=challenge_json, headers=headers)
            if response.status_code in [200, 201]:
                logger.info(f"Level {lvl} generated and saved successfully for user {uid}.")
            else:
                logger.error(f"Failed to save Level {lvl}: {response.text}")
        except Exception as e:
            logger.error(f"Error generating single level {lvl}: {e}")

    background_tasks.add_task(_run_single, level, user_id)
    return {"message": f"Generation started for level {level}"}

@app.post("/hints")
def generate_hint(
    request: HintRequest, 
    x_internal_api_key: Optional[str] = Header(None, alias="X-Internal-API-Key")
):
    logger.info(f"Received hint request for challenge: {request.challenge_slug}")

    if not settings.INTERNAL_API_KEY:
         logger.warning("Internal API Key not configured, skipping auth check (INSECURE)")
    elif x_internal_api_key != settings.INTERNAL_API_KEY:
        logger.warning(f"Unauthorized hint request. Key: {x_internal_api_key}")
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    if not settings.GEMINI_API_KEY and not settings.GROQ_API_KEY:
        logger.error("No LLM API Keys configured")
        raise HTTPException(status_code=500, detail="LLM API Key not configured")

    # 1. Fetch Challenge Context from Core Service
    headers = {"X-Internal-API-Key": settings.INTERNAL_API_KEY}
    try:
        url = f"{settings.CORE_SERVICE_URL}/api/challenges/{request.challenge_slug}/context/"
        logger.info(f"Fetching context from: {url}")
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code != 200:
             logger.error(f"Core service error: {response.status_code} - {response.text}")
             raise HTTPException(status_code=response.status_code, detail=f"Core service returned {response.status_code}")
        
        context_data = response.json()
        logger.info("Context fetched successfully")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to Core Service: {e}")
        raise HTTPException(status_code=503, detail="Core service unavailable")

    # 2. Extract Data
    description = context_data.get("description", "")
    test_code = context_data.get("test_code", "")
    
    # 3. RAG: Search for similar challenges
    logger.info("Performing similarity search for RAG...")
    similar_docs = []
    try:
        query = f"Challenge: {description}\nUser Code: {request.user_code}"
        results = vector_db.similarity_search(query, k=2)
        similar_docs = [doc.page_content for doc in results if doc.metadata.get("slug") != request.challenge_slug]
    except Exception as e:
        logger.warning(f"RAG Search failed: {e}. Proceeding without extra context.")

    # 4. Construct Prompt
    rag_context = "\n\n".join(similar_docs) if similar_docs else "No similar patterns found."
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert coding tutor. Your goal is to provide a helpful hint to a student who is stuck on a coding challenge. "
                   "Do NOT give the direct solution. Analyze their code and the challenge requirements. "
                   "Identify the error or misconception.\n\n"
                   "CONTEXT ENRICHMENT (RAG):\n"
                   "Below are patterns from similar challenges to help you provide a better hint:\n"
                   "{rag_context}\n\n"
                   "ADAPTIVITY RULES:\n"
                   "1. Skill Level: The user has {user_xp} XP. (0-500: Novice, 501-2000: Intermediate, 2000+: Advanced). "
                   "Adjust your vocabulary and explanation depth accordingly.\n"
                   "2. Progressive Depth: This is Level {hint_level} of assistance (1: Strategy/Vague, 2: Logic/Moderate, 3: Implementation/Specific). "
                   "Level 1 should be a gentle nudge. Level 3 can guide them to the exact line or syntax but still not solve it entirely.\n\n"
                   "Be encouraging and concise."),
        ("user", "Challenge Description:\n{description}\n\n"
                 "Test Code:\n{test_code}\n\n"
                 "Student's Code:\n{user_code}\n\n"
                 "Provide a Level {hint_level} hint:")
    ])

    # 5. Call LLM
    try:
        logger.info(f"Initializing LLM via Factory (Provider: {settings.LLM_PROVIDER})")
        from llm_factory import LLMFactory
        
        # Try primary provider
        try:
            llm = LLMFactory.get_llm()
            chain = prompt | llm | StrOutputParser()
            hint = chain.invoke({
                "description": description,
                "test_code": test_code,
                "user_code": request.user_code,
                "hint_level": request.hint_level,
                "user_xp": request.user_xp,
                "rag_context": rag_context
            })
        except Exception as e:
            logger.warning(f"Primary LLM failed: {e}. Attempting fallback...")
            llm = LLMFactory.get_fallback_llm()
            chain = prompt | llm | StrOutputParser()
            hint = chain.invoke({
                "description": description,
                "test_code": test_code,
                "user_code": request.user_code,
                "hint_level": request.hint_level,
                "user_xp": request.user_xp,
                "rag_context": rag_context
            })
            
        logger.info("Hint generated successfully")
        return {"hint": hint}
    except Exception as e:
         logger.error(f"LLM Error (All providers failed): {e}", exc_info=True)
         raise HTTPException(status_code=500, detail="Error generating hint")
