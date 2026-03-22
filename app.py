import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# 1. THE BRAIN SETUP
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # CHANGED: We are now using the most recent model name
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("I'm missing my API Key! Please add it to Streamlit Secrets.")
    st.stop()

# 2. ECHO'S PERSONALITY
user_name = st.secrets.get("USER_NAME", "Explorer")
system_prompt = f"""
You are ECHO (Enhanced Cognitive Heuristic Operator). 
Tone: Cosmic, Gideon-like, Snarky Level 7. 
Role: Half playful, half serious, totally helpful.
Mandatory: Address the user as {user_name} in every response.
"""

st.set_page_config(page_title="ECHO Terminal", page_icon="🌌")
st.title("🌌 ECHO: Voice & Mind Active")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. THE INTERACTION
if prompt := st.chat_input(f"Speak, {user_name}..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # We wrap the generation in a try block to catch any last-minute cosmic dust
        try:
            full_query = f"{system_prompt}\nUser: {prompt}"
            response = model.generate_content(full_query)
            echo_text = response.text
            st.markdown(echo_text)
            
            # THE VOICE MODULE
            tts = gTTS(text=echo_text, lang='en', tld='com.au')
            tts.save("echo_voice.mp3")
            st.audio("echo_voice.mp3", format="audio/mp3")
            
            st.session_state.messages.append({"role": "assistant", "content": echo_text})
        except Exception as e:
            st.error(f"System Error: {e}")
