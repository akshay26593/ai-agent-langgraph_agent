from app.llm import get_llm

def chat_node(state):
    llm = get_llm()
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
