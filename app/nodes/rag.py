from app.vectorstore import load_vectorstore
from langchain.schema import AIMessage

def rag_node(state):
    query = state["messages"][-1].content

    vectorstore = load_vectorstore()
    if not vectorstore:
        return {"messages": [AIMessage(content="No documents uploaded yet.")]}

    docs = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join(d.page_content for d in docs)

    prompt = f"""
Use the context below to answer the question.

Context:
{context}

Question:
{query}
"""

    response = state["llm"].invoke(prompt)
    return {"messages": [response]}
