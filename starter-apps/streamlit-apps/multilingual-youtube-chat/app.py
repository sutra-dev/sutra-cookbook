import os
import streamlit as st
import yt_dlp
import requests
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="YouTube Video Chat",
    page_icon="🎥",
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

# YouTube download options
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': "./%(id)s.%(ext)s",
    'quiet': True,
    'no_warnings': True
}

# AssemblyAI endpoints
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
upload_endpoint = 'https://api.assemblyai.com/v2/upload'
CHUNK_SIZE = 5242880

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
def get_base_chat_model(api_key):
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://api.two.ai/v2",
        model="sutra-v2",
        temperature=0.7,
    )

# Create a streaming version of the model with callback handler
def get_streaming_chat_model(api_key, callback_handler=None):
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://api.two.ai/v2",
        model="sutra-v2",
        temperature=0.7,
        streaming=True,
        callbacks=[callback_handler] if callback_handler else None
    )

# Function to transcribe YouTube video
@st.cache_data
def transcribe_from_link(link):
    try:
        _id = link.strip()
        
        def get_vid(_id):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    return ydl.extract_info(_id)
            except Exception as e:
                st.error(f"Error downloading video: {str(e)}")
                raise Exception("Failed to download video. Please check if the URL is valid.")
        
        # Download the audio
        meta = get_vid(_id)
        save_location = meta['id'] + "." + meta['ext']
        
        def read_file(filename):
            try:
                with open(filename, 'rb') as _file:
                    while True:
                        data = _file.read(CHUNK_SIZE)
                        if not data:
                            break
                        yield data
            except Exception as e:
                st.error(f"Error reading audio file: {str(e)}")
                raise Exception("Failed to read audio file.")
        
        # Upload to AssemblyAI
        try:
            upload_response = requests.post(
                upload_endpoint,
                headers={'authorization': os.getenv('ASSEMBLYAI_API_KEY')},
                data=read_file(save_location)
            )
            upload_response.raise_for_status()
            audio_url = upload_response.json()['upload_url']
        except requests.exceptions.RequestException as e:
            st.error(f"Error uploading to AssemblyAI: {str(e)}")
            raise Exception("Failed to upload audio to AssemblyAI. Please check your API key.")
        
        # Start transcription
        try:
            transcript_request = {
                'audio_url': audio_url,
            }
            
            transcript_response = requests.post(
                transcript_endpoint,
                json=transcript_request,
                headers={
                    'authorization': os.getenv('ASSEMBLYAI_API_KEY'),
                    'content-type': 'application/json'
                }
            )
            transcript_response.raise_for_status()
            transcript_id = transcript_response.json()['id']
            polling_endpoint = transcript_endpoint + "/" + transcript_id
            
            return polling_endpoint
        except requests.exceptions.RequestException as e:
            st.error(f"Error starting transcription: {str(e)}")
            raise Exception("Failed to start transcription. Please check your API key and try again.")
            
    except Exception as e:
        st.error(f"Transcription process failed: {str(e)}")
        raise

# Sidebar configuration
st.sidebar.image("https://framerusercontent.com/images/3Ca34Pogzn9I3a7uTsNSlfs9Bdk.png", use_container_width=True)
with st.sidebar:
    st.markdown("### 🎥 YouTube Video Chat")
    
    # API Keys section in expander
    with st.expander("🔑 API Keys", expanded=False):
        st.markdown("Get your free API keys from:")
        st.markdown("- [SUTRA API](https://www.two.ai/sutra/api)")
        st.markdown("- [AssemblyAI](https://www.assemblyai.com/)")
        
        sutra_api_key = st.text_input("SUTRA API Key:", type="password")
        assembly_api_key = st.text_input("AssemblyAI API Key:", type="password")
    
    # Language selector
    selected_language = st.selectbox("🌐 Chat Language:", languages)
    
    # YouTube URL input
    st.markdown("### 📺 Video Input")
    youtube_url = st.text_input("YouTube URL:")
    
    # Transcribe button
    if youtube_url:
        if st.button("🎬 Transcribe Video", use_container_width=True):
            if not assembly_api_key:
                st.error("Please enter your AssemblyAI API key.")
            else:
                st.session_state.transcription_status = "processing"
                try:
                    # Set environment variable for AssemblyAI
                    os.environ['ASSEMBLYAI_API_KEY'] = assembly_api_key
                    
                    polling_endpoint = transcribe_from_link(youtube_url)
                    
                    # Create a placeholder for status updates
                    status_placeholder = st.empty()
                    
                    # Poll for transcription completion
                    while True:
                        try:
                            polling_response = requests.get(polling_endpoint, headers={'authorization': assembly_api_key})
                            polling_response.raise_for_status()
                            status = polling_response.json()['status']
                            
                            # Update status display
                            status_placeholder.info(f"Status: {status}")
                            
                            if status == 'completed':
                                st.session_state.transcript = polling_response.json()['text']
                                st.session_state.transcription_status = "completed"
                                status_placeholder.empty()
                                st.rerun()
                                break
                            elif status == 'error':
                                error_message = polling_response.json().get('error', 'Unknown error')
                                st.error(f"Error: {error_message}")
                                st.session_state.transcription_status = "error"
                                status_placeholder.empty()
                                st.rerun()
                                break
                            
                            # Update status in session state
                            st.session_state.transcription_status = status
                            time.sleep(2)  # Wait 2 seconds before next poll
                            
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error: {str(e)}")
                            st.session_state.transcription_status = "error"
                            status_placeholder.empty()
                            st.rerun()
                            break
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.session_state.transcription_status = "error"
                    st.rerun()
    
    st.divider()
    st.markdown(f"**Current Language:** {selected_language}")

# Main content
st.markdown(
    f'<h1><img src="https://media.licdn.com/dms/image/v2/C4E0BAQFHAS8MQ9TuJg/company-logo_200_200/company-logo_200_200/0/1674673509083/assemblyai_logo?e=2147483647&v=beta&t=Kvp50eednKAzptWen58EjwigRKmjQZoK4lROa5OZxiY" width="50"/> Multilingual YouTube Chat<img src="https://gifdb.com/images/high/youtube-red-icon-78u4fsgfpf41nvsp.gif" width="100"/></h1>',
    unsafe_allow_html=True
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "transcription_status" not in st.session_state:
    st.session_state.transcription_status = "not_started"

# Video display in expander
if youtube_url:
    with st.expander("View Video", expanded=False):
        st.video(youtube_url)

# Display transcript expander
if youtube_url and st.session_state.transcription_status != "not_started":
    with st.expander("View Video Transcript", expanded=True):
        if st.session_state.transcription_status == "processing":
            st.info("Transcription in progress... Please wait.")
            st.spinner("Processing...")
        elif st.session_state.transcription_status == "completed" and st.session_state.transcript:
            st.success("Transcription completed!")
            st.write(st.session_state.transcript)
        elif st.session_state.transcription_status == "error":
            st.error("Transcription failed. Please try again.")
        else:
            st.info(f"Current status: {st.session_state.transcription_status}")

# Chat interface
if st.session_state.transcript:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    user_input = st.chat_input("Ask questions about the video...")

    # Process user input
    if user_input:
        if not sutra_api_key:
            st.error("Please enter your SUTRA API key in the sidebar.")
        else:
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
                chat = get_streaming_chat_model(sutra_api_key, stream_handler)
                
                # Create system message with context
                system_message = f"""You are a helpful assistant that answers questions about YouTube videos. Please respond in {selected_language}.
                
                IMPORTANT: Use ONLY the information from the video transcript below to answer questions. If the transcript doesn't contain the information needed to answer a question, say so instead of making assumptions.
                
                Video Transcript:
                {st.session_state.transcript}
                
                Instructions:
                1. Base your answers strictly on the video content
                2. If asked about something not covered in the transcript, say "I don't have that information from the video"
                3. Keep answers concise and relevant to the video content
                4. Always respond in {selected_language}
                """
                
                # Generate streaming response
                messages = [
                    SystemMessage(content=system_message),
                    HumanMessage(content=user_input)
                ]
                
                response = chat.invoke(messages)
                answer = response.content
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": answer})
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
                if "API key" in str(e):
                    st.error("Please check your SUTRA API key in the sidebar.")