import streamlit as st
import json
from agent_executor import handle_query

# Set Streamlit page configuration
st.set_page_config(page_title="AI Agent Chat", layout="wide")

st.title("🧑‍💻 AI Agent Chat Interface")
st.write("Chat with your AI agent to execute Python code or analyze CSV data.")
st.header("🤖 What Can This AI Help You With?")
st.markdown("""
This AI agent is designed to assist you with a wide range of topics, including:
- **Python Programming**: Ask it to generate code, debug issues, or explain Python concepts.
- **Data Science with CSV**: Analyze CSV files, generate insights, and perform data manipulations.
- **Tech & IT Jobs of the Future**: Get insights into trending jobs for 2030 and the skills required to excel in them.
- **Programming Languages**: Learn about popular programming languages, their use cases, and which ones to learn.
- **Laptop Prices**: Get up-to-date information on laptop prices based on your requirements.
""")

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

#samples
import streamlit as st
from agent_executor import handle_query

# Title for the section
st.title("Examples")

# List of example prompts
ejemplos = [
    "whic are the columns of it_jobs_2030",
    "What is the most used GPU_model on laptop_prices.csv",
    "What is the mean of salary_in_usd on data science jobs?",
    "Which is the oldest programming language according to languages.csv?",
]

# Dropdown menu for selecting an example
example = st.selectbox("Selecciona un ejemplo:", ejemplos)

# Button to execute the selected example
if st.button("Ejecutar ejemplo"):
    user_input = example

    with st.spinner("Procesando..."):
        try:
            # Get the response from the agent
            answer = handle_query(user_input)
            
            # Display the agent's response
            st.markdown("### Respuesta del agente:")
            
            # Check if the answer is a dictionary with 'output'
            if isinstance(answer, dict) and "output" in answer:
                st.code(answer["output"], language='python')
            else:
                st.markdown(answer)
                
        except ValueError as e:
            st.error(f"Error en el agente: {str(e)}")
