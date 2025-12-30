from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.router import route_selector
from app.nodes.chat import chat_node
from app.nodes.math import math_node
from app.nodes.rag import rag_node

graph = StateGraph(AgentState)

graph.add_node("router", lambda s: s)
graph.add_node("chat", chat_node)
graph.add_node("math", math_node)
graph.add_node("rag", rag_node)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    route_selector,
    {
        "chat": "chat",
        "math": "math",
        "rag": "rag"
    }
)

graph.add_edge("chat", END)
graph.add_edge("math", END)
graph.add_edge("rag", END)

agent = graph.compile()

def run_agent(messages):
    return agent.invoke({"messages": messages})
