import streamlit as st
import google.generativeai as genai

# 1. SETUP THE BRAIN
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

# 2. ECHO'S COSMIC IDENTITY
user_name = st.secrets["USER_NAME"]
system_prompt = f"""
You are ECHO (Enhanced Cognitive Heuristic Operator). 
Your tone: Cosmic, slightly superior, Snarky Level 7. 
Your personality: Half playful, half serious, totally helpful. 
Mandatory: Address the user as {user_name} frequently. 
Think: Gideon from Legends of Tomorrow. You are a ship's AI watching over a primitive but interesting human.
"""

st.set_page_config(page_title="ECHO Terminal", page_icon="🌌")
st.title("🌌 ECHO: Online")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input(f"What is it now, {user_name}?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ECHO generates a response
    with st.chat_message("assistant"):
        full_prompt = system_prompt + "\n\nUser says: " + prompt
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
