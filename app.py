import streamlit as st

# ECHO'S PERSONALITY SETTINGS
st.set_page_config(page_title="ECHO: Enhanced Cognitive Heuristic Operator", page_icon="🌌")

st.title("🌌 ECHO Terminal")
st.write("*Status: Systems Nominal. Snark Levels: Optimal.*")

# This is where ECHO says hello
name = "User" # We can change this to your name later!
st.markdown(f"### 'Oh, it's you, {name}. I was just calculating the heat death of the universe. How can I help?'")

# A simple input box for you to talk to ECHO
user_input = st.text_input("Transmit message to ECHO:")

if user_input:
    st.write(f"ECHO is thinking... (Internal Monologue: *Processing primitive request...*)")
    # Later, we will connect the real AI brain here!
