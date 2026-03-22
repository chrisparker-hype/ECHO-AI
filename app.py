import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# --- THE FIX: FORCING THE API VERSION ---
os.environ["GOOGLE_API_USE_MTLS_ENDPOINT"] = "never"

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # We use 'gemini-1.5-flash' - it is the most stable current model
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key missing! Check Streamlit Secrets.")
    st.stop()

# --- IDENTITY ---
user_name = st.secrets.get("USER_NAME", "Chris")
system_prompt = f"You are ECHO. Cosmic, Gideon-like, Snarky Level 7. Address {user_name}."

st.set_page_config(page_title="ECHO Terminal", page_icon="🌌")
st.title("🌌 ECHO: Online")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(f"Speak, {user_name}..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"{system_prompt}\nUser: {prompt}")
            echo_text = response.text
            st.markdown(echo_text)
            
            tts = gTTS(text=echo_text, lang='en', tld='com.au')
            tts.save("echo_voice.mp3")
            st.audio("echo_voice.mp3")
            
            st.session_state.messages.append({"role": "assistant", "content": echo_text})
        except Exception as e:
            st.error(f"ECHO status check: {str(e)}")
