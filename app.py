import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# 1. THE BRAIN SETUP (The Nuclear Option)
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # We use the most basic name without prefixes
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Brain connection failed: {e}")
        st.stop()
else:
    st.error("API Key missing! Check Streamlit Secrets.")
    st.stop()

# 2. ECHO'S IDENTITY
user_name = st.secrets.get("USER_NAME", "Chris")
system_prompt = f"You are ECHO. Cosmic assistant. Snarky Level 7. Address {user_name}."

st.set_page_config(page_title="ECHO Terminal", page_icon="🌌")
st.title("🌌 ECHO: Online")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. INTERACTION
if prompt := st.chat_input(f"Speak, {user_name}..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # We use 'stream=False' to force a standard response
            response = model.generate_content(f"{system_prompt}\nUser: {prompt}", stream=False)
            echo_text = response.text
            st.markdown(echo_text)
            
            # Voice Generation
            tts = gTTS(text=echo_text, lang='en', tld='com.au')
            tts.save("echo_voice.mp3")
            st.audio("echo_voice.mp3")
            
            st.session_state.messages.append({"role": "assistant", "content": echo_text})
        except Exception as e:
            # If it still fails, we check the EXACT error code
            st.error(f"ECHO status check: {str(e)}")
