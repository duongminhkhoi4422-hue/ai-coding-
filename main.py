from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, PlainTextResponse, FileResponse
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
@app.post("/generate", response_class=PlainTextResponse)
def generate_code(request: CodeRequest):
    return run_code_pipeline(
        problem=request.problem,
        language=request.language
    )


# =============================
# Static Mount (Safe Version)
# =============================
STATIC_DIR = "static"

if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# =============================
# Home Route
# =============================
@app.get("/", response_class=HTMLResponse)
def serve_home():
    file_path = os.path.join(STATIC_DIR, "index.html")

    if os.path.exists(file_path):
        return FileResponse(file_path)

    return """
    <h1>AI Coding Multi-Agent System 🚀</h1>
    <p>Backend running successfully.</p>
    <p>Go to <a href="/docs">/docs</a> for API testing.</p>
    """


# =============================
# Health Check (for Render)
# =============================
@app.get("/health")
def health_check():
    return {"status": "ok"}