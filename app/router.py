import os
from fastapi import APIRouter, UploadFile, File
from app.vectorstore import build_vectorstore

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    chunks = build_vectorstore(file_path)

    return {
        "status": "success",
        "chunks_indexed": chunks,
        "filename": file.filename
    }
