from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from orchestrator_code import run_code_pipeline
import os

app = FastAPI()

# =============================
# CORS
# =============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# Request Schema
# =============================
class CodeRequest(BaseModel):
    problem: str
    language: str

# =============================
# API Endpoint
# =============================
@app.post("/generate")
def generate_code(request: CodeRequest):
    return run_code_pipeline(
        problem=request.problem,
        language=request.language
    )

# =============================
# Serve Web UI
# =============================
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_home():
    if os.path.exists("static/index.html"):
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>AI Coding System Live 🚀</h1><p>Swagger at /docs</p>"