
# backend/nodes/hotels_node.py
from typing import TypedDict
from backend.tools import format_hotels_with_context

class ChatState(TypedDict):
    user_input: str
    ai_response: str

def hotels_node(state: ChatState):
    """Handle hotel/accommodation search queries using RAG + LLM."""
    query = state["user_input"]

    try:
        reply = format_hotels_with_context(query, top_k=5)
    except Exception as e:
        reply = f"Sorry, I couldn't fetch hotel information: {e}"

    return {"ai_response": reply}
