# import streamlit as st
# from backend.graph import create_graph

# # Compile the graph
# app_graph = create_graph()

# # Streamlit page setup
# st.set_page_config(page_title="🌍 Tour Assistant Chatbot", page_icon="🌍")
# st.title("🌍 Tour Assistant Chatbot")

# # Session state for chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display previous messages
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # Chat input
# if user_input := st.chat_input("Ask me about destinations, hotels, weather, or travel tips..."):
#     # Save user message
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     # Run the LangGraph backend
#     result = app_graph.invoke({"user_input": user_input})
#     bot_reply = result["ai_response"]

#     # Save bot message
#     st.session_state.messages.append({"role": "assistant", "content": bot_reply})

#     # Display bot reply
#     with st.chat_message("assistant"):
#         st.markdown(bot_reply)
 # main.py
# app.py
from backend.graph import create_graph

def run_chat():
    graph = create_graph()
    print("🤖 Chatbot is ready! Type 'exit' to quit.")
    state = {"user_input": "", "ai_response": ""}

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        # Set user_input in state so router_node can route properly
        state["user_input"] = user_input

        # Run LangGraph workflow
        result = graph.invoke(state)

        # Get AI reply (each node returns 'ai_response')
        bot_reply = result.get("ai_response", "[No reply]")

        print(f"Bot: {bot_reply}")

        # Update state to keep conversation context if needed
        state = result

if __name__ == "__main__":
    run_chat()
