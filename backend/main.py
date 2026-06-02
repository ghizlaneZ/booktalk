from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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