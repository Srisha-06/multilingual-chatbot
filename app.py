import streamlit as st

st.title("🌍 Multilingual AI Chatbot")

user_input = st.text_input("Enter your message:")

if st.button("Send"):
    if user_input:
        response = "You said: " + user_input
        st.success(response)
    else:
        st.warning("Please enter a message.")
