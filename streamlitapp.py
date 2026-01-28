#This is just to test chatbot UI locally on streamlit
import streamlit as st
import time
try:
    from query import ask_llm_answer
except ImportError:
    def ask_llm_answer(query):
        time.sleep(2) 
        return f"Mock response to: {query}"

st.set_page_config(page_title="My Chatbot", page_icon="🤖")
st.title("🤖 Assistant")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "disabled" not in st.session_state:
    st.session_state.disabled = False


def disable_input():
    st.session_state.disabled = True

for message in st.session_state.messages:
    if isinstance(message, tuple):
        message = {"role": message[0], "content": message[1]}
        
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question...", 
                           disabled=st.session_state.disabled, 
                           on_submit=disable_input):
    

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        with st.spinner("Bot is thinking..."):
            try:
                response = ask_llm_answer(prompt)
            except Exception as e:
                response = f"An error occurred: {e}"
            
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.disabled = False
    st.rerun()