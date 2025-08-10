
# # backend/nodes/chatbot_node.py
# import os
# from typing import TypedDict
# from groq import Groq
# from dotenv import load_dotenv

# # Load environment variables from .env
# load_dotenv()

# # Initialize Groq client
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# class ChatState(TypedDict):
#     user_input: str
#     ai_response: str

# def chatbot_node(state: ChatState):
#     query = state["user_input"]

#     completion = client.chat.completions.create(
#         model="mixtral-8x7b-32768",
#         messages=[
#             {"role": "system", "content": "You are a helpful travel assistant chatbot."},
#             {"role": "user", "content": query}
#         ],
#         temperature=0.7,
#         max_tokens=512
#     )

#     reply = completion.choices[0].message.content
#     return {"ai_response": reply}

# backend/nodes/chatbot_node.py
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
                {"role": "system", "content": "You are a helpful travel assistant chatbot."},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=512
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"Sorry, I couldn't process your request right now: {e}"

    return {"ai_response": reply}


