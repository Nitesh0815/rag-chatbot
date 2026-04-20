from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import pathlib
from dotenv import load_dotenv

load_dotenv()

from app.ingest import ingest_pdf
from app.rag_pipeline import get_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ FIXED: Correct frontend path resolution
# main.py is at /app/app/main.py → .parent = /app/app → .parent = /app → /app/frontend ✅
frontend_dir = pathlib.Path(__file__).parent.parent / "frontend"

if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")
    print(f"✅ Frontend mounted from: {frontend_dir}")
else:
    print(f"⚠️ Frontend dir not found: {frontend_dir}")

class ChatRequest(BaseModel):
    question: str

# ✅ FIXED: Serve index.html at root so browser opens the UI directly
@app.get("/")
async def serve_index():
    index_path = frontend_dir / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "RAG Chatbot API is running. Frontend not found."}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    try:
        temp_path = f"/tmp/temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        ingest_pdf(temp_path)
        os.remove(temp_path)
        return {"message": "PDF ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        answer = get_answer(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}