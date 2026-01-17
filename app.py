import streamlit as st

from query import ask_llm_answer


st.set_page_config(page_title="My Chatbot", page_icon="🤖")
st.title("🤖 My Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_responding" not in st.session_state:
    st.session_state.is_responding = False


for sender, message in st.session_state.messages:
    with st.chat_message("user" if sender == "You" else "assistant"):
        st.markdown(message)


with st.form("chat-input", clear_on_submit=True):
    user_input = st.text_input("You:", "", disabled=st.session_state.is_responding)
    send = st.form_submit_button(
        "Send",
        disabled=st.session_state.is_responding or not user_input.strip(),
        type="primary",
    )

if send and user_input:
    prompt = user_input.strip()
    st.session_state.messages.append(("You", prompt))
    status = st.empty()
    status.info("Received. Bot is thinking...")
    st.session_state.is_responding = True

    with st.spinner("Bot is writing a reply..."):
        response = ask_llm_answer(prompt)

    st.session_state.messages.append(("Bot", response))
    st.session_state.is_responding = False
    status.success("Reply ready.")
    status.empty()
    st.experimental_rerun()
