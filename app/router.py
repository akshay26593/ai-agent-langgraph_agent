import re

def route_selector(state):
    q = state["messages"][-1].content.lower()

    if any(w in q for w in ["emi", "interest", "loan", "statement"]):
        return "rag"

    if re.search(r"\d+[\+\-\*/]\d+", q):
        return "math"

    return "chat"
