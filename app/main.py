from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import os
import shutil

from app.vectorstore import build_vectorstore, load_vectorstore
from app.llm import get_llm

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):
    os.makedirs("data/pdfs", exist_ok=True)
    pdf_path = f"data/pdfs/{file.filename}"

    with open(pdf_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    chunks = build_vectorstore(pdf_path)

    return {
        "status": "success",
        "chunks_indexed": chunks,
        "filename": file.filename
    }


@app.post("/chat")
def chat(req: ChatRequest):
    db = load_vectorstore()
    retriever = db.as_retriever(search_kwargs={"k": 4})

    llm = get_llm()

    docs = retriever.invoke(req.message)
    context = "\n\n".join(d.page_content for d in docs)

    prompt = f"""
    Answer the question using ONLY the context below.

    Context:
    {context}

    Question:
    {req.message}
    """

    response = llm.invoke(prompt)
    return {"reply": response.content}


@app.get("/health")
def health():
    return {"status": "ok"}
