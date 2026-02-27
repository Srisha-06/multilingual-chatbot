import streamlit as st
import requests
from gtts import gTTS
from googletrans import Translator

# Load API key
API_KEY = st.secrets["GROQ_API_KEY"]

API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

translator = Translator()

def generate_reply(user_input):
    # Detect language
    detected = translator.detect(user_input)
    user_lang = detected.lang

    # Translate user input to English
    translated_input = translator.translate(user_input, dest="en").text

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": translated_input}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    if "choices" in result:
        ai_reply_en = result["choices"][0]["message"]["content"]

        # Translate reply back to user's language
        final_reply = translator.translate(ai_reply_en, dest=user_lang).text
        return final_reply
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
