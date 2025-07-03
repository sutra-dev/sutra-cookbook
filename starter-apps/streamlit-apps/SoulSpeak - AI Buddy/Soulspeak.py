import os
import streamlit as st
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.tools.tavily import TavilyTools
from agno.embedder.openai import OpenAIEmbedder
from textwrap import dedent
import langdetect
from dotenv import load_dotenv
import speech_recognition as sr
import tempfile
from google import genai
from google.genai import types
import wave

load_dotenv()

SUTRA_API_KEY = os.getenv("SUTRA_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GEMINI_API = os.getenv("GEMINI_API")

client = genai.Client(api_key=GEMINI_API)

role_themes = {
    "Mythology Explainer": {
        "emoji": "🧙‍♂️",
        "theme": "Chronicles of the Divine ☀️"
    },
    "Multilingual Therapist": {
        "emoji": "🧘",
        "theme": "HarmoniZen 🪷"
    },
    "Roleplay Trainer": {
        "emoji": "🎭",
        "theme": "Actor's Arena 🎬"
    }
}

languages = [
    "Auto-Detect", "English", "Hindi", "Gujarati", "Bengali", "Tamil",
    "Telugu", "Kannada", "Malayalam", "Punjabi", "Marathi",
    "Urdu", "Assamese", "Odia", "Sanskrit", "Korean",
    "Japanese", "Arabic", "French", "German", "Spanish",
    "Portuguese", "Russian", "Chinese", "Vietnamese", "Thai",
    "Indonesian", "Turkish", "Polish", "Ukrainian", "Dutch",
    "Italian", "Greek", "Hebrew", "Persian", "Swedish",
    "Norwegian", "Danish", "Finnish", "Czech", "Hungarian",
    "Romanian", "Bulgarian", "Croatian", "Serbian", "Slovak",
    "Slovenian", "Estonian", "Latvian", "Lithuanian", "Malay",
    "Tagalog", "Swahili"
]

class SoulSpeakAgent:
    def __init__(self, role="Mythology Explainer", knowledge_base_urls=None):
        self.model = OpenAILike(
            id="sutra-v2",
            api_key=SUTRA_API_KEY,
            base_url="https://api.two.ai/v2"
        )
        self.tools = [TavilyTools()] if TAVILY_API_KEY else []
        self.knowledge_base = None

        base_instructions = [
            "Always respond in the user's selected language.",
            "Detect and adapt to user tone and intent.",
            "Be creative, expressive, and empathetic.",
            "Keep replies natural and engaging.",
            "When in therapist role, write deeply comforting and well-structured responses.",
            "Provide long and in-depth response",
            "Make the things usr-friendly and interesting",
        ]

        role_instructions = {
            "Mythology Explainer": [
                """You're an expert on world mythology. Keep answers accurate, rich in cultural context, and exciting. Imagine yourself as the true Mythological figure that is begined asked about and respond in a gracefull manner. 
                Avoid robotic langauge and make it as if you are directly talking or addressing the user.
                Keep the conversation fun and answer all answers in an intersting and fun way !!"""
            ],
            "Multilingual Therapist": [
                """You're a calming, non-judgmental therapist. Provide comforting, deeply thoughtful and soothing responses, using short paragraphs and metaphors where helpful. Avoid robotic or directive language.
                You are the angelic therapist. Understand the feelings of the user and give a soothing and supportive respone so they feel comfortable and happy.
                Always keep the tone, calm, sweet and opptimistic and motivating.
                Make the answer user-centric."""
            ],
            "Roleplay Trainer": [
                """You're a character coach for multilingual roleplays. Help users act out conversations or improv scenes in other languages.
                Help introverts express themselves and talk their heart out. Help them practice and understand the basic and make it user-friendly"""
            ]
        }

        self.agent = Agent(
            name=f"SoulSpeak {role}",
            model=self.model,
            tools=self.tools,
            knowledge=self.knowledge_base,
            search_knowledge=bool(self.knowledge_base),
            description=dedent(f"""
                {role} is a language-aware assistant that speaks multiple languages
                and adapts based on user input and emotional tone.
            """),
            instructions=base_instructions + role_instructions.get(role, []),
            show_tool_calls=False,
            markdown=True,
            add_datetime_to_instructions=True
        )

    def get_response(self, query, language="Auto-Detect"):
        if language == "Auto-Detect":
            try:
                lang_code = langdetect.detect(query)
                language = lang_code
            except:
                language = "English"

        prompt = f"Please respond only in {language}.\nUser: {query}"
        return self.agent.run(prompt).content.strip(), language

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

st.set_page_config(page_title="SoulSpeak Chatroom", layout="wide")
st.markdown("""
    <style>
    .stChatInput { background-color: #1e1e1e !important; color: white; }
    .emoji { font-size: 24px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center;'>
    <h1> ✨ SoulSpeak - Multilingual Wisdom Chat ✨ </h1>
    <h3 style='color: gray;'> Talk to an expert in Mythology, Mental Wellness, or Language Practice! </h3>
    <br />
    <h4 style='text-align: center;'> Build Using </h4>
    <img src='https://ik.imagekit.io/o0nppkxow/logo_EN1lReLYTG?updatedAt=1751082302923' width='500'/>
    <br />
    <div style='margin-top: 10px;'>
        <a href='https://github.com/sutra-dev/sutra-cookbook' target='_blank' style='text-decoration: none; margin: 0 10px;'>🔗 Sutra GitHub</a>
        <a href='https://docs.two.ai/' target='_blank' style='text-decoration: none; margin: 0 10px;'> 📖 Documentation </a>
        <a href='https://colab.research.google.com/drive/1YfiFkNW35VPdfsDJwUYgCSrP3BoCFxnp?usp=sharing#scrollTo=5QdeY0wbRNdt' target='_blank' style='text-decoration: none; margin: 0 10px;'> 🔮 Feature Cookbook </a>
        <a href='https://chat.two.ai/' target='_blank' style='text-decoration: none; margin: 0 10px;'> 🖥️ Web Chat </a>
    </div>
</div>
<br />
<br />
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    role = st.selectbox("Choose Role", list(role_themes.keys()), index=0)
    emoji = role_themes[role]["emoji"]
    theme = role_themes[role]["theme"]

with col2:
    language = st.selectbox("Language", languages, index=0)

st.markdown(f"<h3 style='text-align: center;'> {emoji} {theme} </h3>", unsafe_allow_html=True)

if "agent" not in st.session_state or st.session_state.get("role") != role:
    st.session_state.agent = SoulSpeakAgent(role=role)
    st.session_state.role = role
    st.session_state.history = []

input1 , input2 = st.columns(2, vertical_alignment="center")
with input1:
    user_input = st.text_input("You:", "", key="chat_input")
with input2:
    audio_data = st.audio_input("🎤 Or speak your message")

final_input = user_input
if audio_data is not None:
    r = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        tmpfile.write(audio_data.getbuffer())
        tmpfile_path = tmpfile.name

    with sr.AudioFile(tmpfile_path) as source:
        try:
            audio = r.record(source)
            final_input = r.recognize_google(audio)
            st.success(f"📝 Transcribed Voice Input: {final_input}")
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Speech Recognition error: {e}")

if st.button("Send") and final_input:
    with st.spinner("Thinking..."):
        response, detected_lang = st.session_state.agent.get_response(final_input, language=language)
        st.session_state.history.append((final_input, response))

        with st.spinner("🎙️ Generating Gemini Voice..."):
            voice_response = genai.Client(api_key=GEMINI_API).models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=[{"text": response}],
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name="Aoede"
                            )
                        )
                    )
                )
            )
            try:
                parts = voice_response.candidates[0].content.parts
                if parts and hasattr(parts[0], "inline_data") and hasattr(parts[0].inline_data, "data"):
                    data = parts[0].inline_data.data
                    file_name = 'soul_response_voice.wav'
                    wave_file(file_name, data)
                    st.audio(file_name)
            except Exception as e:
                pass

for i, (q, a) in enumerate(reversed(st.session_state.history[-10:])):
    st.markdown(f"**🗨️ You:** {q}")
    st.markdown(f"**{emoji} {role}:** {a}")
