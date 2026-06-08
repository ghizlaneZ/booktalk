from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.claude_service import ask_question
from pydantic import BaseModel

app = FastAPI(title="BookTalk API", version="1.0.0")

# Permet au frontend React de parler au backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "BookTalk API is running 🎉"}

@app.get("/health", summary="Vérifie que l'API tourne")
def health():
    """Endpoint de santé — utilisé par Kubernetes pour les health checks"""
    return {"status": "ok"}

class QuestionRequest(BaseModel):
    book_content: str
    question: str

@app.post("/ask")
def ask(request: QuestionRequest):
    answer = ask_question(request.book_content, request.question)
    return {"answer": answer}