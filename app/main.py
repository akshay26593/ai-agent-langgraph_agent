from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.agent import run_agent

app = FastAPI(title="AI Agent LangGraph")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    messages = [HumanMessage(content=req.message)]
    result = run_agent(messages)
    return {"reply": result["messages"][-1].content}

@app.get("/health")
def health():
    return {"status": "ok"}
