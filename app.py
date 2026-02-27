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

st.set_page_config(
    page_title="Multilingual AI Chatbot",
    page_icon="🌍",
    layout="centered"
)

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.chat-container {
    padding: 10px;
}

.user-bubble {
    background-color: #0084ff;
    color: white;
    padding: 10px 15px;
    border-radius: 15px;
    margin-bottom: 8px;
    text-align: right;
}

.ai-bubble {
    background-color: #e4e6eb;
    color: black;
    padding: 10px 15px;
    border-radius: 15px;
    margin-bottom: 8px;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

#st.title("🌍 Multilingual AI Voice Chatbot")
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🌍 Multilingual AI Voice Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Real-time AI assistant with multilingual & voice support</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Enter your message (Any Language):")

if st.button("Send") and user_input:
    reply = generate_reply(user_input)

    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("AI", reply))

    # 🔊 Generate voice
    audio_file = speak(reply)
    st.audio(audio_file)

for sender, message in st.session_state.messages:
    if sender == "You":
        st.markdown(f'<div class="user-bubble">🧑 {message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble">🤖 {message}</div>', unsafe_allow_html=True)
