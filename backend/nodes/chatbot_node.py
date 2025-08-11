
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




































# from typing import TypedDict
# from backend.tools import get_groq_client

# # ------------------------
# # Shared state definition
# # ------------------------
# class ChatState(TypedDict):
#     user_input: str
#     ai_response: str
#     user_id: str  # Added for session-based tracking

# # Store conversation state per user
# # In production, replace with a database or session store
# conversation_states = {}

# # Groq client
# client = get_groq_client()

# def call_llm_with_context(user_input: str):
#     """Fallback to Groq LLM for open-ended questions."""
#     try:
#         completion = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are a helpful travel assistant chatbot. "
#                         "Answer concisely and focus only on the requested topic."
#                     )
#                 },
#                 {"role": "user", "content": user_input}
#             ],
#             temperature=0.7,
#             max_tokens=256
#         )
#         return completion.choices[0].message.content
#     except Exception as e:
#         return f"Sorry, I couldn't process your request right now: {e}"

# def chatbot_node(state: ChatState):
#     """Conversation-aware chatbot node with user-specific session tracking."""
#     user_input = state["user_input"].strip().lower()
#     user_id = state["user_id"]

#     # Initialize state for new users
#     if user_id not in conversation_states:
#         conversation_states[user_id] = {
#             "awaiting_topic_choice": False,
#             "location": None
#         }

#     user_state = conversation_states[user_id]

#     # Step 1: Location detection
#     if not user_state["awaiting_topic_choice"]:
#         if "kandy" in user_input:
#             user_state["location"] = "Kandy"
#             user_state["awaiting_topic_choice"] = True
#             reply = (
#                 "Kandy is a beautiful city with rich history and culture. "
#                 "Would you like to know about:\n"
#                 "1. Places to visit\n"
#                 "2. Hotels and accommodation\n"
#                 "3. Things to do\n"
#                 "4. Travel tips\n"
#                 "Please type the number or topic."
#             )
#         else:
#             reply = call_llm_with_context(user_input)

#     # Step 2: Topic choice
#     else:
#         choice = user_input
#         user_state["awaiting_topic_choice"] = False  # Reset after choice

#         if choice in ["1", "places", "places to visit"]:
#             reply = (
#                 "Here are top places to visit in Kandy:\n"
#                 "- Temple of the Tooth\n"
#                 "- Kandy Lake\n"
#                 "- Royal Botanical Gardens\n"
#                 "- Bahirawakanda Temple\n"
#                 "Do you want info about hotels, things to do, or travel tips next?"
#             )
#             user_state["awaiting_topic_choice"] = True
#         elif choice in ["2", "hotels", "accommodation"]:
#             reply = (
#                 "Some budget-friendly hotels in Kandy:\n"
#                 "1. Lake Hotel (4.8/5)\n"
#                 "2. Sky Hotel (4.3/5)\n"
#                 "3. Sun Suites (4.3/5)\n"
#                 "Do you want info about places, things to do, or travel tips next?"
#             )
#             user_state["awaiting_topic_choice"] = True
#         elif choice in ["3", "things to do"]:
#             reply = (
#                 "Popular activities in Kandy:\n"
#                 "- Take a city tour\n"
#                 "- Visit the Kandy Market\n"
#                 "- Attend a cultural show\n"
#                 "- Trek nearby hills\n"
#                 "Do you want info about hotels, places, or travel tips next?"
#             )
#             user_state["awaiting_topic_choice"] = True
#         elif choice in ["4", "travel tips", "tips"]:
#             reply = (
#                 "Travel tips for Kandy:\n"
#                 "- Respect local customs\n"
#                 "- Bargain at markets\n"
#                 "- Use public transport\n"
#                 "Do you want info about hotels, places, or things to do next?"
#             )
#             user_state["awaiting_topic_choice"] = True
#         else:
#             reply = "Please choose 1, 2, 3, or 4."
#             user_state["awaiting_topic_choice"] = True

#     return {"ai_response": reply}