import streamlit as st
import requests
from gtts import gTTS
import os


HF_TOKEN = os.getenv("HF_APITOKEN")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def generate_reply(text):
    output = query({"inputs": text})
    
    if isinstance(output, list):
        return output[0].get("generated_text", "No response generated.")
    else:
        return "Error from AI: " + str(output)

def speak(text):
    tts = gTTS(text=text)
    tts.save("reply.mp3")
    return "reply.mp3"

st.title("🌍 Multilingual AI Voice Chatbot")

user_input = st.text_input("Enter your message (Any Language):")

if st.button("Send"):
    if user_input:
        reply = generate_reply(user_input)
        st.write("🤖 AI Reply:", reply)

        audio_file = speak(reply)
        st.audio(audio_file)
    else:
        st.warning("Please enter a message.")



