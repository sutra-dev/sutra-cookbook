import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("SUTRA_API_KEY")


# Page configuration
st.set_page_config(
    page_title="Sutra Multilingual Chat",
    page_icon="🌐",
    layout="wide"
)

# Define supported languages
languages = [
    "English", "Hindi", "Gujarati", "Bengali", "Tamil", 
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

# Streaming callback handler
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None
    
    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

# Initialize the ChatOpenAI model - base instance for caching
@st.cache_resource
def get_base_chat_model():
    return ChatOpenAI(
        api_key=os.getenv("SUTRA_API_KEY"),
        base_url="https://api.two.ai/v2",
        model="sutra-v2",
        temperature=0.7,
    )

# Create a streaming version of the model with callback handler
def get_streaming_chat_model(callback_handler=None):
    # Create a new instance with streaming enabled
    return ChatOpenAI(
        api_key=os.getenv("SUTRA_API_KEY"),
        base_url="https://api.two.ai/v2",
        model="sutra-v2",
        temperature=0.7,
        streaming=True,
        callbacks=[callback_handler] if callback_handler else None
    )

# Sidebar for language selection
st.sidebar.image("https://framerusercontent.com/images/3Ca34Pogzn9I3a7uTsNSlfs9Bdk.png", use_container_width=True)
with st.sidebar:
    st.title("🌐 Sutra Chat :")
    
    # Language selector
    selected_language = st.selectbox("Select language:", languages)
    
    st.divider()
    st.markdown(f"Currently chatting in: **{selected_language}**")
    
    # About section
    st.markdown("### About Sutra LLM")
    st.markdown("Sutra is a multilingual model supporting 50+ languages with high-quality responses.")

st.markdown(
    f'<h1><img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png" width="60"/> Sutra Multilingual Chatbot 🤖</h1>',
    unsafe_allow_html=True
    )


# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
user_input = st.chat_input("Type your message here...")

# Process user input
if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate response
    try:
        # Create message placeholder
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            # Create a stream handler
            stream_handler = StreamHandler(response_placeholder)
            
            # Get streaming model with handler
            chat = get_streaming_chat_model(stream_handler)
            
            # Create system message indicating preferred language
            system_message = f"You are a helpful assistant. Please respond in {selected_language}."
            
            # Generate streaming response
            messages = [
                HumanMessage(content=f"{system_message}\n\nUser message: {user_input}")
            ]
            
            response = chat.invoke(messages)
            answer = response.content
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": answer})
                
    except Exception as e:
        st.error(f"Error: {str(e)}")
        if "API key" in str(e):
            st.error("Please check your Sutra API key in the environment variables.")
