# import streamlit as st
# from backend.graph import create_graph

# # Compile backend graph
# app_graph = create_graph()

# # Page setup
# st.set_page_config(page_title="🌍 Tour Assistant Chatbot", page_icon="🌍", layout="centered")
# st.title("🌍 Tour Assistant Chatbot")

# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat history
# for msg in st.session_state.messages:
#     avatar = "🧑‍💼" if msg["role"] == "user" else "🤖"
#     with st.chat_message(msg["role"], avatar=avatar):
#         st.markdown(msg["content"])

# # Chat input
# if user_input := st.chat_input("Ask me about destinations, hotels, weather, or travel tips..."):
#     # Show user message immediately
#     with st.chat_message("user", avatar="🧑‍💼"):
#         st.markdown(user_input)
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     # Show "bot is typing" placeholder
#     with st.chat_message("assistant", avatar="🤖"):
#         typing_placeholder = st.empty()
#         typing_placeholder.markdown("💭 Thinking of the best travel tips for you...")

#         # Get bot response
#         result = app_graph.invoke({"user_input": user_input})
#         bot_reply = result["ai_response"]

#         # Replace placeholder with actual bot reply
#         typing_placeholder.markdown(bot_reply)

#     # Save bot message
#     st.session_state.messages.append({"role": "assistant", "content": bot_reply})


import streamlit as st
from backend.graph import create_graph

# Compile backend graph
app_graph = create_graph()

# Page setup
st.set_page_config(page_title="🌍 Tour Assistant Chatbot", page_icon="🌍", layout="centered")
st.title("🌍 Tour Assistant Chatbot")

# Dark/light mode-friendly CSS
st.markdown("""
    <style>
    .user-msg {
        text-align: right;
        background-color: rgba(0, 123, 255, 0.2); /* bluish bubble */
        color: inherit;
        padding: 10px;
        border-radius: 10px;
        display: inline-block;
        margin: 5px;
        max-width: 70%;
    }
    .bot-msg {
        text-align: left;
        background-color: rgba(255, 255, 255, 0.1); /* light grey bubble */
        color: inherit;
        padding: 10px;
        border-radius: 10px;
        display: inline-block;
        margin: 5px;
        max-width: 70%;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
    }
    .user-container {
        display: flex;
        justify-content: flex-end;
    }
    .bot-container {
        display: flex;
        justify-content: flex-start;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-container"><div class="user-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-container"><div class="bot-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)

# Chat input
if user_input := st.chat_input("Ask me about destinations, hotels, weather, or travel tips..."):
    # Save and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="user-container"><div class="user-msg">{user_input}</div></div>', unsafe_allow_html=True)

    # Get bot response
    result = app_graph.invoke({"user_input": user_input})
    bot_reply = result["ai_response"]

    # Save and display bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.markdown(f'<div class="bot-container"><div class="bot-msg">{bot_reply}</div></div>', unsafe_allow_html=True)




 # main.py
# app.py
# from backend.graph import create_graph

# def run_chat():
#     graph = create_graph()
#     print("🤖 Chatbot is ready! Type 'exit' to quit.")
#     state = {"user_input": "", "ai_response": ""}

#     while True:
#         user_input = input("You: ").strip()
#         if user_input.lower() in ["exit", "quit"]:
#             print("👋 Goodbye!")
#             break

#         # Set user_input in state so router_node can route properly
#         state["user_input"] = user_input

#         # Run LangGraph workflow
#         result = graph.invoke(state)

#         # Get AI reply (each node returns 'ai_response')
#         bot_reply = result.get("ai_response", "[No reply]")

#         print(f"Bot: {bot_reply}")

#         # Update state to keep conversation context if needed
#         state = result

# if __name__ == "__main__":
#     run_chat()
