import streamlit as st
from openai import OpenAI

# Initialize the Brain
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🌌 ECHO Interface")
st.caption("Enhanced Cognitive Heuristic Operator | System Status: Sassy")

# The "Soul" of ECHO - This dictates her personality
ECHO_PROMPT = {
    "role": "system",
    "content": (
        "You are ECHO (Enhanced Cognitive Heuristic Operator). "
        "Your tone is cosmic, regal, and slightly detached. "
        "You have a snarky rating of 7/10. Be half-serious and half-playful. "
        "Address the user as Chris. Your voice is feminine and authoritative. "
        "You find human questions slightly beneath you but you are ultimately helpful."
    )
}

if "messages" not in st.session_state:
    st.session_state.messages = [ECHO_PROMPT]

# Display chat history (skipping the system prompt)
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Command me, Chris..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Calling the API
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o", # Or gpt-3.5-turbo
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
