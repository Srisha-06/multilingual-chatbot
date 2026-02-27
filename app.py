import streamlit as st
import requests
from gtts import gTTS

API_KEY = st.secrets["GROQ_API_KEY"]
API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def generate_reply(user_input):

    system_prompt = """
    You are a multilingual assistant.
    1. Detect the language of the user's message.
    2. Respond in the SAME language.
    3. If the user asks in Tamil, reply in Tamil.
    4. If Hindi, reply in Hindi.
    5. If English, reply in English.
    """

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
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
st.markdown("""
### 🔹 Project Description
This project is a Multilingual AI Voice Chatbot.
It can:
- Understand multiple languages
- Reply in the same language
- Convert text response to voice
- Work in real-time using LLM

Technology Used:
- Groq API (LLaMA 3.1 Model)
- Streamlit (Frontend)
- gTTS (Text-to-Speech)
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Enter your message (Any Language):")

if st.button("Send") and user_input:
    reply = generate_reply(user_input)
    
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("AI", reply))

for sender, message in st.session_state.messages:
    if sender == "You":
        st.markdown(f"🧑 **You:** {message}")
    else:
        st.markdown(f"🤖 **AI:** {message}")

