from app.vectorstore import load_vectorstore
from app.llm import get_llm

def run_agent(query: str) -> str:
    vectordb = load_vectorstore()
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    docs = retriever.get_relevant_documents(query)
    context = "\n\n".join([d.page_content for d in docs])

    llm = get_llm()

    prompt = f"""
Use the context below to answer the question.

Context:
{context}

Question:
{query}
"""

    return llm.invoke(prompt).content
