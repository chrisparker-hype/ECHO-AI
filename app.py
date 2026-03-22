import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# 1. THE BRAIN SETUP (Stable Legacy Version)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Using the standard 'gemini-pro' which is universally available
    model = genai.GenerativeModel('gemini-pro') 
else:
    st.error("I'm missing my API Key! Check Streamlit Secrets.")
    st.stop()

# 2. ECHO'S IDENTITY
user_name = st.secrets.get("USER_NAME", "Chris")
system_prompt = f"""
You are ECHO (Enhanced Cognitive Heuristic Operator). 
Tone: Cosmic, Gideon-like, Snarky Level 7. 
Address the user as {user_name}.
"""

st.set_page_config(page_title="ECHO Terminal", page_icon="🌌")
st.title("🌌 ECHO: Online")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. INTERACTION
if prompt := st.chat_input(f"Transmit message, {user_name}..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # We are using a very direct generation method here
            full_query = f"{system_prompt}\nUser: {prompt}"
            response = model.generate_content(full_query)
            echo_text = response.text
            st.markdown(echo_text)
            
            # Voice Generation
            tts = gTTS(text=echo_text, lang='en', tld='com.au')
            tts.save("echo_voice.mp3")
            st.audio("echo_voice.mp3")
            
            st.session_state.messages.append({"role": "assistant", "content": echo_text})
        except Exception as e:
            # If it fails, ECHO will tell us exactly why in plain English
            st.error(f"ECHO status check: {str(e)}")
