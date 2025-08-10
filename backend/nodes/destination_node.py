
# backend/nodes/destination_node.py
from typing import TypedDict
from backend.tools import recommend_destinations

class ChatState(TypedDict):
    user_input: str
    ai_response: str

def destination_node(state: ChatState):
    """Suggest travel destinations based on user's preferences."""
    query = state["user_input"]

    try:
        destinations = recommend_destinations(query, n=5)
        formatted = "\n".join([f"{i+1}. {d}" for i, d in enumerate(destinations)])
    except Exception as e:
        formatted = f"Sorry, I couldn't find destinations right now: {e}"

    return {"ai_response": formatted}
