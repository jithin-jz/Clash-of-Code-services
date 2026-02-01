from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="AI Service",
    version="1.0",
    root_path="/ai"
)

class Prompt(BaseModel):
    prompt: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/complete")
def complete(data: Prompt):
    # placeholder for real LLM logic
    return {
        "input": data.prompt,
        "output": f"AI response to: {data.prompt}"
    }
