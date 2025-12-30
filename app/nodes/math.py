import sympy as sp
from langchain_core.messages import AIMessage

def math_node(state):
    q = state["messages"][-1].content
    try:
        result = sp.simplify(q)
        return {"messages": [AIMessage(content=str(result))]}
    except:
        return {"messages": [AIMessage(content="I don't know")]}
