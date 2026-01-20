from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="CodeShorts AI Service")

@app.get("/")
def read_root():
    return {"status": "AI Service Running", "service": "AI"}

@app.post("/generate")
def generate_text(prompt: str):
    # Placeholder for AI logic
    return {"result": f"AI response for: {prompt}", "model": "Mock-AI"}
