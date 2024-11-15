import streamlit as st
import json
from agent_executor import handle_query

# Set Streamlit page configuration
st.set_page_config(page_title="AI Agent Chat", layout="wide")

st.title("🧑‍💻 AI Agent Chat Interface")
st.write("Chat with your AI agent to execute Python code or analyze CSV data.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to display chat messages
def display_chat():
    for role, message in st.session_state.messages:
        if role == "user":
            st.markdown(f"**🧑‍💻 You:** {message}")
        else:
            st.markdown(f"**🤖 Agent:**")
            if isinstance(message, dict):
                # Display dictionary response in a formatted way
                st.json(message)
            else:
                st.markdown(message)

# Display existing chat messages
display_chat()

# Simple input box for user query
user_input = st.text_input("Type your message and press Enter", key="user_input")

# Check if user has entered a message
if user_input:
    # Store user message in session state
    st.session_state.messages.append(("user", user_input))
    
    with st.spinner("Processing..."):
        try:
            # Get response from the agent
            response = handle_query(user_input)
            
            
            
            # Store agent response in session state
            if isinstance(response, dict):
                st.session_state.messages.append(("agent", response["output"]))
            else:
                st.session_state.messages.append(("agent", {"output": response}))
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Display updated chat messages
st.write("---")
display_chat()
