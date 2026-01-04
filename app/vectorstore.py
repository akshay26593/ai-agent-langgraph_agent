import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

VECTOR_DIR = "data/index"

# ✅ Fully local embeddings (NO internet)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def build_vectorstore(pdf_path: str) -> int:
    os.makedirs(VECTOR_DIR, exist_ok=True)

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(VECTOR_DIR)

    return len(chunks)

def load_vectorstore():
    if not os.path.exists(VECTOR_DIR):
        raise RuntimeError("Vectorstore not found. Upload a PDF first.")

    try:
        return FAISS.load_local(
            VECTOR_DIR,
            embeddings,
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        print("⚠️ Corrupted FAISS index, deleting:", e)
        shutil.rmtree(VECTOR_DIR)
        raise RuntimeError("Vectorstore corrupted. Please upload PDF again.")
