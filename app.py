import streamlit as st
from gtts import gTTS
import random

st.title("🌍 Multilingual AI Voice Chatbot")

user_input = st.text_input("Enter your message (Any Language):")

def generate_reply(text):
    responses = [
        "That's interesting!",
        "Can you tell me more?",
        "I understand what you're saying.",
        "That sounds great!",
        "Let me think about that.",
        "Here is what I believe about it."
    ]
    return random.choice(responses)

def speak(text):
    tts = gTTS(text=text)
    tts.save("reply.mp3")
    return "reply.mp3"

if st.button("Send"):
    if user_input:
        reply = generate_reply(user_input)
        st.write("🤖 AI Reply:", reply)

        audio_file = speak(reply)
        st.audio(audio_file)
    else:
        st.warning("Please enter a message.")
