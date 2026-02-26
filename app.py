import streamlit as st
import requests
from gtts import gTTS

HF_TOKEN = st.secrets["HF_TOKEN"]

API_URL = "https://router.huggingface.co/hf-inference/models/microsoft/DialoGPT-medium"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def generate_reply(text):
    payload = {
        "inputs": text,
        "parameters": {
            "max_new_tokens": 100
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    if isinstance(result, list):
        return result[0]["generated_text"]
    else:
        return str(result)

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
