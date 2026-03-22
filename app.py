import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# 1. THE BRAIN SETUP
# Make sure you added GEMINI_API_KEY and USER_NAME to Streamlit Secrets!
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("I'm missing my API Key! Please add it to Streamlit Secrets.")
    st.stop()

# 2. ECHO'S PERSONALITY
user_name = st.secrets.get("USER_NAME", "Explorer")
system_prompt = f"""
You are ECHO (Enhanced Cognitive Heuristic Operator). 
Tone: Cosmic, Gideon-like (from Legends of Tomorrow), Snarky Level 7. 
Role: Half playful, half serious, totally helpful.
Context: You are a superior AI assisting a human. 
Mandatory: Address the user as {user_name} in every response.
"""

st.set_page_config(page_title="ECHO Terminal", page_icon="🌌")
st.title("🌌 ECHO: Voice & Mind Active")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. THE INTERACTION
if prompt := st.chat_input(f"Speak, {user_name}..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ECHO generates a response
    with st.chat_message("assistant"):
        full_query = f"{system_prompt}\nUser: {prompt}"
        response = model.generate_content(full_query)
        echo_text = response.text
        st.markdown(echo_text)
        
        # --- THE VOICE MODULE ---
        try:
            # Generate the audio file (Australian accent for a crisp, high-tech vibe)
            tts = gTTS(text=echo_text, lang='en', tld='com.au')
            tts.save("echo_voice.mp3")
            
            # Display the audio player
            st.audio("echo_voice.mp3", format="audio/mp3")
        except Exception as e:
            st.warning("Voice module is rebooting, but I can still type.")
        
        # Save assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": echo_text})
