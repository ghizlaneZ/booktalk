# FastAPI est le framework web ; File/UploadFile gèrent les fichiers entrants ; HTTPException renvoie des erreurs HTTP propres
from fastapi import FastAPI, File, UploadFile, HTTPException
# Middleware qui autorise le frontend React (autre origine) à appeler ce backend
from fastapi.middleware.cors import CORSMiddleware
from services.claude_service import ask_question
from services.pdf_parser import extract_text_from_pdf
# BaseModel de Pydantic valide automatiquement le JSON reçu dans les requêtes
from pydantic import BaseModel

app = FastAPI(title="BookTalk API", version="1.0.0")

# Sans ce middleware, le navigateur bloquerait les requêtes venant de localhost:3000 vers localhost:8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # seul le frontend React est autorisé
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "BookTalk API is running 🎉"}

@app.get("/health", summary="Vérifie que l'API tourne")
def health():
    return {"status": "ok"}

# Pydantic vérifie que la requête JSON contient bien ces deux champs avec le bon type
class QuestionRequest(BaseModel):
    book_content: str
    question: str

# async permet de lire le fichier sans bloquer les autres requêtes en attendant l'I/O
@app.post("/upload", summary="Upload un PDF et retourne son texte extrait")
async def upload_pdf(file: UploadFile = File(...)):
    # File(...) signifie que le champ est obligatoire (les ... sont la syntaxe Pydantic pour "requis")
    if not file.filename.endswith(".pdf"):
        # 400 Bad Request : le client a envoyé un type de fichier non supporté
        raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont acceptés")
    # Lit tout le contenu binaire du fichier uploadé en mémoire
    content = await file.read()
    text = extract_text_from_pdf(content)
    if not text:
        # 422 Unprocessable Entity : le fichier est valide mais son contenu ne peut pas être traité
        raise HTTPException(status_code=422, detail="Impossible d'extraire du texte de ce PDF")
    return {"filename": file.filename, "text": text}


@app.post("/ask")
def ask(request: QuestionRequest):
    answer = ask_question(request.book_content, request.question)
    return {"answer": answer}
