import streamlit as st
import time

# Function loader
try:
    from query import ask_llm_answer
except ImportError:
    def ask_llm_answer(query):
        time.sleep(2) 
        return f"Mock response to: {query}"

# --- Page Configuration ---
st.set_page_config(page_title="My Chatbot", page_icon="🤖")
st.title("🤖 Assistant")

# --- 1. Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize the 'disabled' flag to False (Input is active by default)
if "disabled" not in st.session_state:
    st.session_state.disabled = False

# --- 2. Helper Function to Lock UI ---
# This runs immediately when the user hits Enter, before the script reloads
def disable_input():
    st.session_state.disabled = True

# --- Display Chat History ---
for message in st.session_state.messages:
    # (Includes the fix for the tuple error you saw earlier)
    if isinstance(message, tuple):
        message = {"role": message[0], "content": message[1]}
        
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. Locked User Input ---
# We bind the 'disabled' state to the widget and use 'on_submit' to trigger the lock
if prompt := st.chat_input("Ask a question...", 
                           disabled=st.session_state.disabled, 
                           on_submit=disable_input):
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display bot response
    with st.chat_message("assistant"):
        with st.spinner("Bot is thinking..."):
            try:
                response = ask_llm_answer(prompt)
            except Exception as e:
                response = f"An error occurred: {e}"
            
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

    # --- 4. Unlock and Refresh ---
    # Now that processing is done, unlock the input and rerun to update the UI
    st.session_state.disabled = False
    st.rerun()