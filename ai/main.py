from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(title="CodeShorts AI Service")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExplainRequest(BaseModel):
    code: str
    language: str = "python"

@app.get("/")
def read_root():
    return {"status": "AI Service Running", "service": "AI"}

@app.post("/explain")
async def explain_code(request: ExplainRequest):
    """
    Simulates AI code explanation.
    In the future, replace this with calls to OpenAI/Gemini/Anthropic.
    """
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    # Simulate processing delay
    # time.sleep(1) 

    # Mock Response Logic
    explanation = f"This appears to be {request.language} code. "
    explanation += "Here is a breakdown of what it does:\n\n"
    explanation += "1. **Analysis**: The code performs a specific operation.\n"
    explanation += "2. **Complexity**: It seems efficient.\n"
    explanation += "3. **Optimization**: Consider checking for edge cases.\n\n"
    explanation += "(Note: This is a placeholder AI response. Connect an API key to get real insights!)"

    return {
        "explanation": explanation,
        "model": "CodeShorts-Mini-v1 (Mock)",
        "tokens_used": len(request.code.split())
    }
