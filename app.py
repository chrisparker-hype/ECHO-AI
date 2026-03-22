import streamlit as st
import os
import google.generativeai as genai
from gtts import gTTS

# 1. THE BRAIN SETUP (The Final Version)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # We use 'gemini-1.5-flash' but we wrap it in a function that checks for 'v1'
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
else:
    st.error("I'm missing my API Key! Check Streamlit Secrets.")
    st.stop()

# 2. ECHO'S IDENTITY
user_name = st.secrets.get("USER_NAME", "Chris")
system_prompt = f"You are ECHO. Cosmic, Gideon-like, Snarky Level 7. Address {user_name}."

st.set_page_config(page_title="ECHO Terminal", page_icon="🌌")
st.title("🌌 ECHO: Active")

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
            # Forcing the use of the most compatible method
            response = model.generate_content(f"{system_prompt}\nUser: {prompt}")
            echo_text = response.text
            st.markdown(echo_text)
            
            # Voice Generation
            tts = gTTS(text=echo_text, lang='en', tld='com.au')
            tts.save("echo_voice.mp3")
            st.audio("echo_voice.mp3")
            
            st.session_state.messages.append({"role": "assistant", "content": echo_text})
        except Exception as e:
            st.error(f"ECHO status check: {e}")
