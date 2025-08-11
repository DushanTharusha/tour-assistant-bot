from typing import TypedDict
from backend.tools import get_groq_client

# Shared state definition for chatbot nodes
class ChatState(TypedDict):
    user_input: str
    ai_response: str

# Get Groq API client from tools.py
client = get_groq_client()

def chatbot_node(state: ChatState):
    """General chatbot conversation node using Groq LLM."""
    query = state["user_input"]

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant chatbot. "
                 "Please respond briefly and only provide a small piece of information at a time. "
                 "After your response, ask the user if they want more details or other topics. "
                 "Wait for the user's confirmation before providing additional information."
                 "Strictly Stay with Travel Domain"},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=512
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"Sorry, I couldn't process your request right now: {e}"

    return {"ai_response": reply}

































