# # backend/graph.py
# from typing import TypedDict
# from langgraph.graph import StateGraph, START, END

# # Import your nodes
# from backend.nodes.chatbot_node import chatbot_node
# from backend.nodes.hotels_node import hotels_node
# from backend.nodes.destination_node import destination_node
# from backend.nodes.weather_node import weather_node

# # ----- Define the State -----
# class ChatState(TypedDict):
#     user_input: str
#     ai_response: str

# # ----- Simple Router -----
# def router_node(state: ChatState):
#     """Route user queries to the right node based on keywords."""
#     user_q = state["user_input"].lower()
#     if not user_q:
#         return {"route": "fallback"}  # or handle empty input case

#     if any(word in user_q for word in ["hotel", "stay", "accommodation"]):
#         next_node = "hotels"
#     elif any(word in user_q for word in ["destination", "recommend", "where to go", "place to visit"]):
#         next_node = "destinations"
#     elif any(word in user_q for word in ["weather", "temperature", "forecast"]):
#         next_node = "weather"
#     else:
#         next_node = "chatbot"

#     return {"next": next_node}

# # ----- Build the Graph -----
# def create_graph():
#     workflow = StateGraph(ChatState)

#     # Add nodes
#     workflow.add_node("router", router_node)
#     workflow.add_node("chatbot", chatbot_node)
#     workflow.add_node("hotels", hotels_node)
#     workflow.add_node("destinations", destination_node)
#     workflow.add_node("weather", weather_node)

#     # Edges
#     workflow.add_edge(START, "router")
#     workflow.add_conditional_edges(
#         "router",
#         lambda state: router_node(state)["next"],
#         {
#             "chatbot": "chatbot",
#             "hotels": "hotels",
#             "destinations": "destinations",
#             "weather": "weather",
#         }
#     )

#     # All nodes end after execution
#     workflow.add_edge("chatbot", END)
#     workflow.add_edge("hotels", END)
#     workflow.add_edge("destinations", END)
#     workflow.add_edge("weather", END)

#     return workflow.compile()





from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from backend.nodes.chatbot_node import chatbot_node
from backend.nodes.hotels_node import hotels_node
from backend.nodes.destination_node import destination_node
from backend.nodes.weather_node import weather_node

class ChatState(TypedDict):
    user_input: str
    ai_response: str
    next: str  # added so router_node output can be reused

def router_node(state: ChatState):
    """Route user query to the right node based on keywords."""
    user_q = state.get("user_input", "").lower().strip()

    if not user_q:
        return {"next": "chatbot"}

    if any(w in user_q for w in ["hotel", "stay", "accommodation"]):
        return {"next": "hotels"}
    elif any(w in user_q for w in ["destination", "recommend", "where to go", "place to visit"]):
        return {"next": "destinations"}
    elif any(w in user_q for w in ["weather", "temperature", "forecast"]):
        return {"next": "weather"}
    else:
        return {"next": "chatbot"}

def create_graph():
    workflow = StateGraph(ChatState)

    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("chatbot", chatbot_node)
    workflow.add_node("hotels", hotels_node)
    workflow.add_node("destinations", destination_node)
    workflow.add_node("weather", weather_node)

    # Define edges
    workflow.add_edge(START, "router")
    workflow.add_conditional_edges(
        "router",
        lambda state: state["next"],  # Use the computed value from router_node
        {
            "chatbot": "chatbot",
            "hotels": "hotels",
            "destinations": "destinations",
            "weather": "weather",
        }
    )

    # End edges
    workflow.add_edge("chatbot", END)
    workflow.add_edge("hotels", END)
    workflow.add_edge("destinations", END)
    workflow.add_edge("weather", END)

    return workflow.compile()


# # backend/graph.py
# from typing import TypedDict
# from langgraph.graph import StateGraph, START, END

# from backend.nodes.chatbot_node import chatbot_node
# from backend.nodes.hotels_node import hotels_node
# from backend.nodes.destination_node import destination_node
# from backend.nodes.weather_node import weather_node

# # ---- New: Refusal node for out-of-domain queries ----
# def refusal_node(state: dict):
#     return {
#         "ai_response": (
#             "I’m your travel assistant. Please ask travel-related questions such as "
#             "destinations, hotels, or weather."
#         )
#     }

# class ChatState(TypedDict):
#     user_input: str
#     ai_response: str
#     next: str

# # ---- Updated Router with domain restriction ----
# def router_node(state: ChatState):
#     user_q = state.get("user_input", "").lower().strip()

#     if not user_q:
#         return {"next": "refusal"}  # no input → refusal

#     travel_keywords = [
#         "hotel", "stay", "accommodation", "destination", "recommend",
#         "where to go", "place to visit", "weather", "temperature", "forecast"
#     ]

#     if any(word in user_q for word in ["hotel", "stay", "accommodation"]):
#         return {"next": "hotels"}
#     elif any(word in user_q for word in ["destination", "recommend", "where to go", "place to visit"]):
#         return {"next": "destinations"}
#     elif any(word in user_q for word in ["weather", "temperature", "forecast"]):
#         return {"next": "weather"}
#     elif any(word in user_q for word in travel_keywords):
#         return {"next": "chatbot"}  # general travel query
#     else:
#         return {"next": "refusal"}  # out-of-domain

# def create_graph():
#     workflow = StateGraph(ChatState)

#     # Add nodes
#     workflow.add_node("router", router_node)
#     workflow.add_node("chatbot", chatbot_node)
#     workflow.add_node("hotels", hotels_node)
#     workflow.add_node("destinations", destination_node)
#     workflow.add_node("weather", weather_node)
#     workflow.add_node("refusal", refusal_node)  # new node

#     # Start → Router
#     workflow.add_edge(START, "router")

#     # Conditional routing
#     workflow.add_conditional_edges(
#         "router",
#         lambda state: state["next"],
#         {
#             "chatbot": "chatbot",
#             "hotels": "hotels",
#             "destinations": "destinations",
#             "weather": "weather",
#             "refusal": "refusal",
#         }
#     )

#     # End edges
#     workflow.add_edge("chatbot", END)
#     workflow.add_edge("hotels", END)
#     workflow.add_edge("destinations", END)
#     workflow.add_edge("weather", END)
#     workflow.add_edge("refusal", END)

#     return workflow.compile()