import streamlit as st
import requests
from gtts import gTTS
import os

# --- 1. SETTINGS ---
api_key = st.secrets["GEMINI_API_KEY"]
user_name = st.secrets.get("USER_NAME", "Chris")
# The "Direct Line" URL
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

st.set_page_config(page_title="ECHO Terminal", page_icon="🌌")
st.title("🌌 ECHO: Direct Link Active")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 2. THE INTERACTION ---
if prompt := st.chat_input(f"Speak, {user_name}..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Preparing the "Letter" to the AI
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"You are ECHO. Cosmic assistant. Snarky Level 7. Address {user_name}. User says: {prompt}"
                    }]
                }]
            }
            
            # Sending the request
            response = requests.post(url, json=payload)
            result = response.json()
            
            # Extracting the text
            echo_text = result['candidates'][0]['content']['parts'][0]['text']
            st.markdown(echo_text)
            
            # Voice Generation
            tts = gTTS(text=echo_text, lang='en', tld='com.au')
            tts.save("echo_voice.mp3")
            st.audio("echo_voice.mp3")
            
            st.session_state.messages.append({"role": "assistant", "content": echo_text})
            
        except Exception as e:
            st.error(f"ECHO is offline. Error: {result if 'result' in locals() else e}")
