import streamlit as st
import os
import gc
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import time
import pandas as pd
from typing import Dict, Any
import base64
from pydantic import BaseModel, Field
import inspect
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.callbacks.base import BaseCallbackHandler
from langdetect import detect

def scrape_website(url: str, prompt: str) -> str:
    """Scrape website content using BeautifulSoup."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        raise Exception(f"Error scraping website: {str(e)}")

# Page configuration
st.set_page_config(
    page_title="Multilingual Website Data Extractor",
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

# Language code mapping
language_codes = {
    "English": "en", "Hindi": "hi", "Gujarati": "gu", "Bengali": "bn", "Tamil": "ta",
    "Telugu": "te", "Kannada": "kn", "Malayalam": "ml", "Punjabi": "pa", "Marathi": "mr",
    "Urdu": "ur", "Assamese": "as", "Odia": "or", "Sanskrit": "sa", "Korean": "ko",
    "Japanese": "ja", "Arabic": "ar", "French": "fr", "German": "de", "Spanish": "es",
    "Portuguese": "pt", "Russian": "ru", "Chinese": "zh", "Vietnamese": "vi", "Thai": "th",
    "Indonesian": "id", "Turkish": "tr", "Polish": "pl", "Ukrainian": "uk", "Dutch": "nl",
    "Italian": "it", "Greek": "el", "Hebrew": "he", "Persian": "fa", "Swedish": "sv",
    "Norwegian": "no", "Danish": "da", "Finnish": "fi", "Czech": "cs", "Hungarian": "hu",
    "Romanian": "ro", "Bulgarian": "bg", "Croatian": "hr", "Serbian": "sr", "Slovak": "sk",
    "Slovenian": "sl", "Estonian": "et", "Latvian": "lv", "Lithuanian": "lt", "Malay": "ms",
    "Tagalog": "tl", "Swahili": "sw"
}

# Streaming callback handler
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None
    
    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

load_dotenv()
sutra_api_key = os.getenv("SUTRA_API_KEY")

@st.cache_resource
def get_chat_model():
    if not st.session_state.get("sutra_api_key"):
        raise ValueError("SUTRA API key is not set. Please enter your API key in the sidebar.")
    
    return ChatOpenAI(
        api_key=st.session_state.sutra_api_key,
        base_url="https://api.two.ai/v2",
        model="sutra-v2",
        temperature=0.7,
    )

def translate_text(text: str, target_lang: str = "en") -> str:
    """Translate text to target language using Sutra model."""
    try:
        chat = get_chat_model()
        # Make the translation prompt more specific and strict
        prompt = f"""Translate the following text to {target_lang}. 
        Important: 
        1. Only provide the translation, no explanations
        2. Maintain the exact same format and structure
        3. If it's a table, keep the table format
        4. If it's a list, keep the list format
        5. Ensure the output is strictly in {target_lang} language
        6. Do not include any other language in the response
        7. If the text is already in {target_lang}, return it as is
        
        Text to translate: {text}"""
        response = chat.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
    except ValueError as ve:
        st.error(str(ve))
        return text
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "urls" not in st.session_state:
    st.session_state.urls = [""]  # Initialize with one empty URL

def add_url():
    st.session_state.urls.append("")

def remove_url(index):
    if len(st.session_state.urls) > 1:  # Keep at least one URL input
        st.session_state.urls.pop(index)

def reset_chat():
    st.session_state.messages = []
    gc.collect()

def convert_to_table(data):
    """Convert a list of dictionaries to a simple markdown table."""
    if not data:
        return ""
    
    if isinstance(data, dict):
        data = [data]
    elif isinstance(data, list):
        pass
    else:
        return ""
    
    df = pd.DataFrame(data)
    return df.to_markdown(index=False)

def stream_text(text: str, delay: float = 0.001) -> None:
    """Stream text with a typing effect."""
    placeholder = st.empty()
    displayed_text = ""
    
    for char in text:
        displayed_text += char
        placeholder.markdown(displayed_text)
        time.sleep(delay)
    
    return placeholder

# Main content area
st.markdown(
    f'<h1><img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png" width="60" style="vertical-align: middle;"/>Multilingual Chat via URLs <img src="https://i.gifer.com/3WyW.gif" width="80" height="80" style="vertical-align: middle;"/></h1>',
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # API Key sections
    st.markdown("### 🔑 API Keys")
    st.markdown("#### 🤖 SUTRA API")
    st.markdown("Get your free API key from [SUTRA API](https://www.two.ai/sutra/api) 🔗")
    sutra_api_key = st.text_input("Enter your Sutra API Key:", 
                                  value=st.session_state.get("sutra_api_key", ""),
                                  type="password",
                                  label_visibility="collapsed")
    if sutra_api_key:
        st.session_state.sutra_api_key = sutra_api_key
    
    # Language selector
    st.markdown("### 🌍 Language Settings")
    selected_language = st.selectbox("Select output language:", languages)
    
    # Website URLs input with plus button
    st.markdown("### 🔗 Website URLs")
    for i, url in enumerate(st.session_state.urls):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.session_state.urls[i] = st.text_input(
                f"🌐 URL {i+1}",
                value=url,
                placeholder="https://example.com",
                key=f"url_{i}"
            )
        with col2:
            if i == len(st.session_state.urls) - 1:  # Only show plus button on last URL input
                st.button("➕", key=f"add_{i}", on_click=add_url)
            if len(st.session_state.urls) > 1:  # Show remove button if more than one URL
                st.button("➖", key=f"remove_{i}", on_click=lambda i=i: remove_url(i))
    
    # Add a divider
    st.markdown("---")
    
    # Add expandable tips section
    with st.expander("💡 Click here for helpful tips"):
        st.markdown("""
        ### How to use this app:
        
        📌 **URL Management:**
        - Use the ➕ button to add more URLs
        - Use the ➖ button to remove URLs
        - You can analyze multiple websites at once
        
        🌐 **Language Features:**
        - Ask questions in any language
        - Get responses in your preferred language
        - Automatic language detection
        
        """)

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about the website in any language..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # Filter out empty URLs
        valid_urls = [url for url in st.session_state.urls if url.strip()]
        
        if not valid_urls:
            st.error("Please enter at least one website URL!")
        elif not st.session_state.get("sutra_api_key"):
            st.error("Please enter your SUTRA API key in the sidebar!")
        else:
            try:
                with st.spinner("Processing your request..."):
                    # Get target language code
                    target_lang = language_codes[selected_language]
                    
                    # Detect input language
                    input_lang = detect(prompt)
                    
                    # Translate to English if not already in English
                    if input_lang != 'en':
                        translated_prompt = translate_text(prompt, "en")
                    else:
                        translated_prompt = prompt
                    
                    # Process all valid URLs
                    all_data = []
                    for url in valid_urls:
                        try:
                            # Scrape website content
                            content = scrape_website(url, translated_prompt)
                            
                            # Use the chat model to analyze the content based on the prompt
                            chat = get_chat_model()
                            analysis_prompt = f"""Based on the following website content, answer this question: {translated_prompt}
                            
                            Website content:
                            {content}
                            
                            Please provide a clear and concise answer."""
                            
                            response = chat.invoke([HumanMessage(content=analysis_prompt)])
                            all_data.append(response.content)
                            
                        except Exception as e:
                            st.warning(f"Error processing URL {url}: {str(e)}")
                            continue
                    
                    if not all_data:
                        st.error("No data could be extracted from any of the provided URLs.")
                    else:
                        # Combine all data
                        if len(all_data) == 1:
                            response = str(all_data[0])
                        else:
                            response = "\n\n".join([f"Results from {url}:\n{str(data)}" 
                                                  for url, data in zip(valid_urls, all_data)])
                        
                        # Always translate to selected language if not English
                        if target_lang != 'en':
                            # Add a verification step for translation
                            st.info(f"Translating to {selected_language}...")
                            response = translate_text(response, target_lang)
                            
                            # Verify the translation
                            detected_lang = detect(response)
                            if detected_lang != target_lang:
                                # If translation is not in the correct language, try again with more strict prompt
                                st.warning(f"Detected language ({detected_lang}) doesn't match target language ({target_lang}). Retrying translation...")
                                response = translate_text(response, target_lang)
                        
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your API key and try again.")