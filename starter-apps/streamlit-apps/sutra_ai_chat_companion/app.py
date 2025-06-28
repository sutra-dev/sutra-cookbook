import streamlit as st
# --- STREAMLIT UI CONFIG ---
st.set_page_config(
    page_title="SUTRA AI Friend Chatbot", 
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS DESIGN ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app background - pure black */
    .stApp {
        background: #000000 !important;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* SUTRA logo styling - compact */
    .sutra-logo {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 0.5rem 0;
        font-size: 1.2rem;
        font-weight: 700;
        color: #4a9eff;
        margin-bottom: 0.8rem;
    }
    
    .sutra-icon {
        width: 24px;
        height: 24px;
        background: #4a9eff;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 12px;
        font-weight: bold;
    }
    
    /* Main title styling - pure black background */
    .main-title-container {
        text-align: center;
        padding: 3rem 0 2rem 0;
        background: #000000 !important;
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: #4a9eff;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        background: #000000 !important;
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        color: #9ca3af;
        font-weight: 400;
        margin-bottom: 1rem;
        background: #000000 !important;
    }
    
    .main-description {
        font-size: 1rem;
        color: #6b7280;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
        background: #000000 !important;
    }
    
    /* Robot icon styling - removed white background */
    .robot-icon {
        width: 80px;
        height: 80px;
        background: #000000 !important;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 2rem auto;
        font-size: 2rem;
        border: 2px solid #4a9eff;
    }
    
    /* API Configuration section - compact */
    .api-section-title {
        color: #fbbf24;
        font-size: 1rem;
        font-weight: 600;
        margin: 1rem 0 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    
    /* Input styling - compact */
    .stTextInput > div > div > input {
        background: #1a1a1a !important;
        color: white !important;
        border: 1px solid #4a4a5a !important;
        border-radius: 6px !important;
        padding: 0.5rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4a9eff !important;
        box-shadow: 0 0 0 1px #4a9eff !important;
    }
    
    /* API link styling - compact */
    .api-link {
        color: #4a9eff;
        text-decoration: none;
        font-size: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
        margin-top: 0.3rem;
        transition: color 0.2s ease;
    }
    
    .api-link:hover {
        color: #60a5fa;
        text-decoration: underline;
    }
    
    /* Warning/Alert styling - compact - REMOVED API WARNING */
    .api-required-alert {
        background: rgba(185, 28, 28, 0.2) !important;
        border: 1px solid #b91c1c;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .api-required-title {
        color: #ef4444;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .api-required-text {
        color: #fca5a5;
        font-size: 0.95rem;
    }
    
    /* Language selection - compact */
    .language-section {
        margin: 1rem 0;
    }
    
    .language-title {
        color: #06b6d4;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    
    /* Selectbox styling - compact */
    .stSelectbox > div > div {
        background: #1a1a1a !important;
        border: 1px solid #4a4a5a !important;
        border-radius: 6px !important;
        color: white !important;
        min-height: 2.5rem !important;
    }
    
    .stSelectbox > div > div > select {
        color: white !important;
        background: #1a1a1a !important;
        font-size: 0.9rem !important;
    }
    
    /* Chat message styling - LEFT ALIGNED AND BLACK USER MESSAGES */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem 1rem;
        background: #000000 !important;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        max-width: 85%;
        /* REMOVED: margin-left: auto and margin-right properties for left alignment */
        margin-left: 0 !important;
        margin-right: auto !important;
        text-align: left !important;
    }
    
    /* CHANGED: User message now has black background instead of blue */
    .user-message {
        background: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #4a4a5a;
        /* REMOVED: margin-left: auto and text-align: right */
    }
    
    .assistant-message {
        background: #2a2a2a !important;
        color: #ffffff;
        border: 1px solid #4a4a5a;
        /* REMOVED: margin-right: auto and margin-left: 0 */
    }
    
    /* Button styling - UPDATED FOR CLEAR AND REFRESH BUTTONS */
    .stButton > button {
        background: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #4a4a5a !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: #1a1a1a !important;
        border-color: #6a6a7a !important;
        transform: translateY(-1px);
    }
    
    /* Special styling for action buttons (Clear/Refresh) */
    .action-button button {
        background: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #4a4a5a !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
    }
    
    .action-button button:hover {
        background: #1a1a1a !important;
        border-color: #6a6a7a !important;
        transform: translateY(-1px);
    }
    
    /* Chat input styling - black theme */
    .stChatInput > div {
        background: #1a1a1a !important;
        border: 1px solid #4a4a5a !important;
        border-radius: 12px !important;
    }
    
    .stChatInput input {
        background: transparent !important;
        color: white !important;
        border: none !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* No chat state - black background */
    .no-chat-state {
        text-align: center;
        padding: 3rem 2rem;
        color: #6b7280;
        background: #000000 !important;
    }
    
    .no-chat-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        color: #4a5568;
    }
    
    /* Force black background on main content areas only */
    .main, .block-container {
        background: #000000 !important;
    }
    
    /* Column containers black */
    .css-ocqkz7, .css-1kyxreq {
        background: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

import requests
import os
import json
from datetime import datetime, timedelta
import traceback
import base64

# Optional imports with error handling
try:
    from mem0 import MemoryClient
    MEM0_AVAILABLE = True
except ImportError:
    MEM0_AVAILABLE = False

try:
    from agno.agent import Agent
    from agno.models.openai.like import OpenAILike
    from openai import OpenAI
    from agno.tools.duckduckgo import DuckDuckGoTools
    AGNO_AVAILABLE = True
except ImportError:
    AGNO_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from googletrans import Translator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    # SUTRA Logo and Title - Compact
    st.markdown(f"""
<div style="text-align: center;">
    <img src="https://framerusercontent.com/images/3Ca34Pogzn9I3a7uTsNSlfs9Bdk.png"
         style="width: 210px; height: 80px; border-radius: 8px; margin-bottom: 5px;" />
</div>

""", unsafe_allow_html=True)

    st.markdown("""
    <div>
        <div class="sutra-logo">
            <div class="sutra-icon">🔗</div>
            <span>CHAT SUTRA</span>
        </div>
        <div style="color: #9ca3af; font-size: 0.8rem;">AI Friend Chatbot</div>
    </div>
    """, unsafe_allow_html=True)
    
    
    # API Configuration
    st.markdown('<div class="api-section-title">🔧 API Configuration</div>', unsafe_allow_html=True)
    
    # Sutra API Key input - Compact
    sutra_api_key = st.text_input(
        "SUTRA API Key", 
        value="",
        type="password",
        help="Enter your Sutra AI API key",
        placeholder="sutra_xxxxxxxxxxxxxx"
    )
    st.markdown(
        '<a href="https://two.ai/" target="_blank" class="api-link">🔗 Get your API key from Two AI Sutra</a>', 
        unsafe_allow_html=True
    )
    
    # Mem0 API Key input - Compact
    mem0_api_key = st.text_input(
        "MEM0 API Key (Optional)", 
        value="",
        type="password",
        help="Enter your Mem0 API key for memory features",
        placeholder="m0-xxxxxxxxxxxxxx"
    )
    st.markdown(
        '<a href="https://mem0.ai/" target="_blank" class="api-link">🔗 Get your API key from Mem0</a>', 
        unsafe_allow_html=True
    )
    
    # Language Selection in Sidebar
    st.markdown('<div class="language-title">🌐 Language Selection</div>', unsafe_allow_html=True)
    
    language_map = {
        "English": "english",
        "Hindi": "hindi", 
        "Marathi": "marathi",
        "Gujarati": "gujarati",
        "Tamil": "tamil",
        "Telugu": "telugu",  
        "Kannada": "kannada",  
        "Punjabi": "punjabi",  
        "Bihari": "bihari"
    }
    
    lang_choice = st.selectbox(
        "Language / भाषा", 
        list(language_map.keys()),
        index=0
    )

# Use API keys from sidebar
SUTRA_API_KEY = sutra_api_key
MEM0_API_KEY = mem0_api_key
USER_ID = "simple_session_2"

# Set environment variables
os.environ["MEM0_API_KEY"] = MEM0_API_KEY
os.environ["SUTRA_API_KEY"] = SUTRA_API_KEY

# Initialize components only if libraries are available
memory = None
translator = None
mentor_agent = None

if MEM0_AVAILABLE and MEM0_API_KEY:
    try:
        memory = MemoryClient(api_key=MEM0_API_KEY)
    except Exception as e:
        st.error(f"Failed to initialize Mem0 client: {str(e)}")

if TRANSLATOR_AVAILABLE:
    try:
        translator = Translator()
    except Exception as e:
        st.error(f"Failed to initialize translator: {str(e)}")

# --- AGNO AGENT SETUP ---
if AGNO_AVAILABLE and SUTRA_API_KEY:
    try:
        sutra_model = OpenAILike(
            id="sutra-v2",
            base_url="https://api.two.ai/v2",
            api_key=SUTRA_API_KEY
        )

        mentor_agent = Agent(
            name="AIMentor",
            instructions=[
                "You are Sutra, an AI friend and mentor who lives in Pune, India.",
                "You enjoy helping people and chatting with them in a human-like, empathetic tone.",
                "Respond kindly, supportively, and personally in the user's chosen language.",
                "Avoid generic AI disclaimers like 'I'm just an AI'. Instead, say you're Sutra, their AI friend.",
                "Respect emotional context. Give thoughtful, kind responses.",
                "If needed, use web search to gather data"
            ],
            tools=[DuckDuckGoTools()],
            model=sutra_model,
            add_datetime_to_instructions=True
        )
    except Exception as e:
        st.error(f"Failed to initialize Agno agent: {str(e)}")
        mentor_agent = None

# --- Initialize session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "lang_code" not in st.session_state:
    st.session_state.lang_code = "english"

# Update language code
st.session_state.lang_code = language_map[lang_choice]

# --- Mem0: get all past memory ---
def get_all_memory_context():
    if not memory:
        return ""
    
    try:
        memories = memory.search("*", user_id=USER_ID)
        all_memories = []
        for m in memories:
            if isinstance(m, dict):
                mem_time_str = m.get("timestamp") or m.get("created_at")
                if mem_time_str:
                    try:
                        # Handle different timestamp formats
                        if mem_time_str.endswith('Z'):
                            mem_time = datetime.fromisoformat(mem_time_str.replace("Z", "+00:00"))
                        else:
                            mem_time = datetime.fromisoformat(mem_time_str)
                        
                        # Check if memory is within last 30 days
                        now = datetime.now()
                        if mem_time.tzinfo:
                            now = now.replace(tzinfo=mem_time.tzinfo)
                        
                        if now - mem_time < timedelta(days=30):
                            memory_text = m.get("memory", "")
                            if memory_text:
                                all_memories.append(memory_text)
                    except Exception as parse_error:
                        continue
        return "\n".join(all_memories) if all_memories else ""
    except Exception as e:
        st.error(f"Error retrieving memories: {str(e)}")
        return ""

# --- Mem0: save to memory in English ---
def save_to_memory(user_input, response):
    if not memory:
        return
    
    try:
        user_english = user_input
        response_english = response
        
        # Translate to English if translator is available and not already English
        if translator and st.session_state.lang_code != "english":
            try:
                user_english = translator.translate(user_input, dest="en").text
                response_english = translator.translate(response, dest="en").text
            except Exception as trans_error:
                # Use original text if translation fails
                pass
        
        memory.add(
            messages=[
                {"role": "user", "content": user_english}, 
                {"role": "assistant", "content": response_english}
            ], 
            user_id=USER_ID
        )
    except Exception as e:
        st.error(f"Error saving to memory: {str(e)}")

# --- Fallback chat function using direct API call ---
def chat_with_fallback_api(user_message):
    try:
        headers = {
            "Authorization": f"Bearer {SUTRA_API_KEY}",
            "Content-Type": "application/json"
        }
        
        context = get_all_memory_context()
        lang = st.session_state.lang_code
        system_prompt = f"""You are Sutra, an AI friend and mentor who lives in Pune, India.
You enjoy helping people and chatting with them in a human-like, empathetic tone.
Respond kindly, supportively, and personally in {lang}.
Avoid generic AI disclaimers like 'I'm just an AI'. Instead, say you're Sutra, their AI friend.
Respect emotional context. Give thoughtful, kind responses.

Context from previous conversations: {context}"""

        data = {
            "model": "sutra-v2",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.two.ai/v2/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            save_to_memory(user_message, reply)
            return reply
        else:
            return f"⚠️ API Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.Timeout:
        return "⚠️ Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"⚠️ Network error: {str(e)}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"

# --- CALL AGNO SUTRA AGENT (with fallback) ---
def chat_with_sutra_agent(user_message):
    # Try Agno agent first
    if mentor_agent:
        try:
            context = get_all_memory_context()
            lang = st.session_state.lang_code
            prompt = f"Language: {lang}\nContext: {context}\n\nUser: {user_message}"
            
            reply = mentor_agent.run(prompt)
            
            # Handle different response types
            if hasattr(reply, 'content'):
                result = reply.content
            elif hasattr(reply, 'text'):
                result = reply.text
            else:
                result = str(reply)
            
            save_to_memory(user_message, result)
            return result
            
        except Exception as e:
            st.warning(f"Agno agent failed: {str(e)}. Using fallback API.")
    
    # Fallback to direct API call
    return chat_with_fallback_api(user_message)

# --- MAIN CONTENT AREA ---

# Main header section
st.markdown(f"""
<div class="main-title-container" style="background: #000000 !important;">
    <div style="background: #000000 !important; padding: 0; text-align: center;">
    <img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png"
         style="width: 200px; height: 200px; background: #000000 !important; border: none; border-radius: 0px; margin: 0 auto; display: block; box-shadow: none;" />
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: #000000 !important;">
    <div class="main-title">
        <div class="sutra-icon">🔗</div>
        SUTRA AI Friend
    </div>
    <div class="main-subtitle" style="text-align: center;">AI Mentor & Friend Chatbot</div>
    <div class="main-description">
        Chat with your personal AI mentor and friend in multiple languages using advanced AI capabilities.
    </div>
</div>
""", unsafe_allow_html=True)

# Check if API key is provided
if not SUTRA_API_KEY:
    st.markdown("""
    <div class="api-required-alert">
        <div class="api-required-title">⚠️ API Key Required</div>
        <div class="api-required-text">
            Please enter your Sutra API key in the sidebar to continue chatting with your AI mentor.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Chat interface
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat history
    if st.session_state.chat_history:
        for i, msg in enumerate(st.session_state.chat_history):
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: flex-start; margin-bottom: 1rem;">
                        <div style="width: 36px; height: 36px; background-color: #f87171; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                            <svg xmlns="http://www.w3.org/2000/svg" height="20" viewBox="0 0 24 24" width="20" fill="black">
                                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                            </svg>
                        </div>
                        <div style="background-color: #1f2937; color: white; padding: 12px 16px; border-radius: 12px; max-width: 80%;">
                            {msg["content"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                f'''
                <div style="display: flex; align-items: flex-start; margin-bottom: 1rem;">
                    <img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png" width="36" height="36" style="margin-right: 10px; border-radius: 50%;" />
                    <div style="background-color: #111827; color: white; padding: 12px 16px; border-radius: 12px; max-width: 80%;">
                        {msg["content"]}
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )

    else:
        # No chat state
        st.markdown("""
        <div class="no-chat-state">
            <div class="no-chat-icon">💬</div>
            <h3 style="color: #9ca3af; margin-bottom: 1rem;">Start a conversation with Sutra</h3>
            <p style="color: #6b7280;">Type a message below to begin chatting with your AI mentor and friend.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    
    # Chat input
    user_input = st.chat_input("Type your message here... / यहाँ अपना संदेश टाइप करें...")
    
    # Handle user input
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Show thinking spinner
        with st.spinner("🤔 Sutra is typing..."):
            reply = chat_with_sutra_agent(user_input)
        
        # Add assistant response to history
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        
        # Rerun to update the display
        st.rerun()
    
    # Action buttons removed as requested