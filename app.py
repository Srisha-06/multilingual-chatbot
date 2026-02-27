import streamlit as st
import requests
from gtts import gTTS

# Load API key from secrets
API_KEY = st.secrets["GROQ_API_KEY"]

API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def generate_reply(user_input):
    payload = {
    "model": "llama-3.1-8b-instant",
    "messages": [
        {"role": "user", "content": user_input}
    ]
}

    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {result}"

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


