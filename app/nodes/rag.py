from langchain_core.messages import AIMessage
from app.llm import get_llm
from app.prompts import RAG_PROMPT

def rag_node(state):
    llm = get_llm()
    question = state["messages"][-1].content
    response = llm.invoke(question)
    return {"messages": [AIMessage(content=response.content)]}
