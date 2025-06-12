import streamlit as st
import requests
import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.callbacks.base import BaseCallbackHandler

# Page configuration
st.set_page_config(
    page_title="Global News Hub",
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

# Streaming callback handler for Sutra LLM
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
        temperature=0.3,  # Lower temperature for more accurate translations
    )

# Create a streaming version of the model with callback handler
def get_streaming_chat_model(api_key, callback_handler=None):
    # Create a new instance with streaming enabled
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://api.two.ai/v2",
        model="sutra-v2",
        temperature=0.3,  # Lower temperature for more accurate translations
        streaming=True,
        callbacks=[callback_handler] if callback_handler else None
    )

# Function to fetch high-quality image using Serper Images API
def fetch_high_quality_image(query):
    url = "https://google.serper.dev/images"
    payload = json.dumps({
        "q": query,
        "num": 1  # We only need one image
    })
    headers = {
        'X-API-KEY': st.session_state.serper_api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
        results = response.json()
        if results.get("images") and len(results["images"]) > 0:
            return results["images"][0].get("imageUrl")
        return None
    except Exception as e:
        st.warning(f"Error fetching high-quality image: {str(e)}")
        return None

# Function to fetch news using Serper API
def fetch_news(query, num_results=10, language=None, page=1):
    url = "https://google.serper.dev/news"
    payload = {
        "q": query,
        "num": num_results
    }
    
    # Add optional parameters if provided
    if language:
        payload["hl"] = language
    if page > 1:
        payload["page"] = page
        
    payload = json.dumps(payload)
    headers = {
        'X-API-KEY': st.session_state.serper_api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        results = response.json()
        news_items = results.get("news", [])
        
        # Enhance news items with high-quality images
        enhanced_news_items = []
        for item in news_items:
            # Try to get a high-quality image based on the title
            high_quality_image = fetch_high_quality_image(item.get('title', ''))
            if high_quality_image:
                item['imageUrl'] = high_quality_image
            enhanced_news_items.append(item)
        
        return enhanced_news_items
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {str(e)}")
        return []

# Function to translate news using Sutra LLM
def translate_news(news_items, target_language, api_key):
    try:
        # Get base model (non-streaming) for translation
        model = get_base_chat_model(api_key)
        
        # Create a container for all news articles
        news_container = st.container()
        
        # Process each news item individually
        translated_items = []
        for i, item in enumerate(news_items):
            # Store original image URL
            original_image_url = item.get('imageUrl')
            
            # Create a specific prompt for each news item
            system_message = f"""
            You are a professional translator specializing in news translation. Translate the following news content to {target_language}.
            
            Translation Rules:
            1. Translate ONLY these fields:
               - title: Keep it concise and engaging
               - snippet: Maintain the news context and tone
               - source: Translate the source name if it has a common translation
            
            2. Translation Guidelines:
               - Ensure natural and fluent language
               - Maintain the original meaning and context
               - Keep any proper nouns (names, places) in their original form
               - Preserve any numbers, dates, and measurements
               - Keep any technical terms accurate
            
            3. Return ONLY the translated fields in this exact format:
            {{
                "title": "translated title",
                "snippet": "translated snippet",
                "source": "translated source"
            }}
            
            4. Important:
               - Do not add any explanations
               - Do not modify the JSON structure
               - Do not translate any other fields
               - Ensure the translation is culturally appropriate for {target_language} speakers
            """
            
            # Prepare only the fields that need translation
            fields_to_translate = {
                "title": item.get('title', ''),
                "snippet": item.get('snippet', ''),
                "source": item.get('source', '')
            }
            
            # Convert to JSON string
            item_json = json.dumps(fields_to_translate, ensure_ascii=False)
            
            # Generate response
            messages = [
                HumanMessage(content=f"{system_message}\n\nFields to translate:\n{item_json}")
            ]
            
            try:
                # Show processing status
                with st.spinner(f"Translating article {i+1} of {len(news_items)}..."):
                    response = model.invoke(messages)
                    result = response.content.strip()
                    
                    # Clean the response
                    result = result.replace('```json', '').replace('```', '').strip()
                    
                    # Parse the translated fields
                    translated_fields = json.loads(result)
                    
                    # Create new item with translated fields and original data
                    translated_item = {
                        **item,  # Keep all original fields
                        "title": translated_fields.get('title', item.get('title', '')),
                        "snippet": translated_fields.get('snippet', item.get('snippet', '')),
                        "source": translated_fields.get('source', item.get('source', '')),
                        "imageUrl": original_image_url  # Ensure original image is kept
                    }
                    
                    translated_items.append(translated_item)
                    
                    # Display the translated article with improved layout
                    with news_container:
                        # Create a card-like container for each article
                        with st.container():
                            # Create two columns with adjusted ratio
                            col1, col2 = st.columns([3, 2])
                            
                            # Left column for text content
                            with col1:
                                st.markdown(f"### {i+1}. {translated_item['title']}")
                                st.markdown(f"**Source:** {translated_item['source']} | {translated_item.get('date', 'Unknown date')}")
                                st.markdown(translated_item['snippet'])
                                st.markdown(f"[Read more]({translated_item['link']})")
                            
                            # Right column for image with fixed height
                            with col2:
                                if original_image_url:  # Use original image URL
                                    # Add custom CSS for image container
                                    st.markdown("""
                                        <style>
                                        .image-container {
                                            height: 200px;
                                            overflow: hidden;
                                            border-radius: 10px;
                                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                                        }
                                        .image-container img {
                                            width: 100%;
                                            height: 100%;
                                            object-fit: cover;
                                        }
                                        </style>
                                        """, unsafe_allow_html=True)
                                    
                                    # Wrap image in styled container
                                    st.markdown(f"""
                                        <div class="image-container">
                                            <img src="{original_image_url}" alt="News Image">
                                        </div>
                                        """, unsafe_allow_html=True)
                            
                            st.divider()
                            
            except json.JSONDecodeError as e:
                st.warning(f"Failed to parse translation of item {i+1}: {str(e)}. Using original.")
                translated_items.append(item)
            except Exception as e:
                st.warning(f"Error translating item {i+1}: {str(e)}. Using original.")
                translated_items.append(item)
        
        return translated_items
            
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return news_items

# Function to format news as markdown
def format_news_as_markdown(news_items):
    markdown = ""
    for i, news in enumerate(news_items):
        markdown += f"### {i+1}. {news.get('title', 'No Title')}\n\n"
        markdown += f"**Source:** {news.get('source', 'Unknown')} | {news.get('date', 'Unknown date')}\n\n"
        markdown += f"{news.get('snippet', 'No description available.')}\n\n"
        markdown += f"[Read more]({news.get('link', '#')})\n\n"
        if news.get('imageUrl'):
            markdown += f"![News Image]({news.get('imageUrl')})\n\n"
        markdown += "---\n\n"
    return markdown

# Function to translate search query to English using Sutra LLM
def translate_query_to_english(query, api_key):
    try:
        # Get base model (non-streaming) for translation
        model = get_base_chat_model(api_key)
        
        system_message = """
        You are a professional translator. Translate the following search query to English.
        
        Translation Rules:
        1. Keep the translation concise and clear
        2. Maintain the search intent
        3. Preserve any proper nouns (names, places)
        4. Keep any numbers, dates, and measurements
        5. Ensure the translation is natural and search-friendly
        
        Return ONLY the translated query without any explanations or additional text.
        """
        
        messages = [
            HumanMessage(content=f"{system_message}\n\nQuery to translate:\n{query}")
        ]
        
        response = model.invoke(messages)
        translated_query = response.content.strip()
        
        return translated_query
        
    except Exception as e:
        st.warning(f"Error translating query: {str(e)}. Using original query.")
        return query

# Initialize session state variables
if "serper_api_key" not in st.session_state:
    st.session_state.serper_api_key = ""
if "sutra_api_key" not in st.session_state:
    st.session_state.sutra_api_key = ""
if "news_data" not in st.session_state:
    st.session_state.news_data = []
if "search_query" not in st.session_state:
    st.session_state.search_query = "latest news Updates on AI"

# Sidebar for settings
with st.sidebar:
    st.markdown(
        f'<h1>🌎 Global News Hub</h1>',
        unsafe_allow_html=True
    )
    
    # API Key sections
    st.markdown("### API Keys")
    st.markdown("**SUTRA API**")
    st.markdown("Get your free API key from [SUTRA API](https://www.two.ai/sutra/api)")
    sutra_api_key = st.text_input("Enter your Sutra API Key:", 
                                  value=st.session_state.sutra_api_key,
                                  type="password",
                                  label_visibility="collapsed")
    if sutra_api_key:
        st.session_state.sutra_api_key = sutra_api_key
    
    st.markdown("**Serper API**")
    st.markdown("Get your API key from [Serper.dev](https://serper.dev/)")
    serper_api_key = st.text_input("Enter your Serper API Key:", 
                                   value=st.session_state.serper_api_key,
                                   type="password",
                                   label_visibility="collapsed")
    if serper_api_key:
        st.session_state.serper_api_key = serper_api_key
    
    # Number of results selector
    st.markdown("### Search Settings")
    num_results = st.slider("Number of news articles to display:", 
                           min_value=5, 
                           max_value=30, 
                           value=10, 
                           step=5,
                           help="Select how many news articles you want to see")
    
    # Language selector
    st.markdown("### Language Settings")
    selected_language = st.selectbox("Select language:", languages)
    
    st.divider()
    st.markdown(f"Currently viewing news in: **{selected_language}**")
    
    # About section
    with st.expander("About Global News Hub"):
        st.markdown("""
        This app uses:
        - **Serper API** to fetch the latest news from around the world
        - **Sutra LLM** to translate news into 50+ languages
        - **Streamlit** for the interactive web interface
        
        Search for any topic and get news updates in your preferred language!
        """)

# Main content area
st.markdown(
    f'<h1><img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png" width="60" style="vertical-align: middle;"/> Multilingual News Hub <img src="https://media.baamboozle.com/uploads/images/821733/1656648869_810178_gif-url.gif" width="70" height="70" style="vertical-align: middle;"/></h1>',
    unsafe_allow_html=True
)

# Search bar
col1, col2 = st.columns([4, 1])
with col1:
    search_query = st.text_input("Search for news:", value=st.session_state.search_query)
with col2:
    search_button = st.button("Search", type="primary", use_container_width=True)

# Validate API keys before searching
if search_button or (not st.session_state.news_data and st.session_state.serper_api_key):
    if not st.session_state.serper_api_key:
        st.error("Please enter your Serper API key in the sidebar.")
    else:
        st.session_state.search_query = search_query
        
        # Translate query to English if needed
        if selected_language != "English" and st.session_state.sutra_api_key:
            with st.spinner("Translating search query to English..."):
                english_query = translate_query_to_english(search_query, st.session_state.sutra_api_key)
                st.info(f"Translated query: '{english_query}'")
        else:
            english_query = search_query
        
        # Show loading message
        with st.spinner(f"Fetching news for '{english_query}'..."):
            # Fetch news data
            news_items = fetch_news(
                query=english_query,
                num_results=num_results,
                language=selected_language.lower() if selected_language != "English" else None
            )
            
            if news_items:
                st.session_state.news_data = news_items
                st.success(f"Found {len(news_items)} news articles!")
            else:
                st.warning("No news found. Try a different search term.")

# Display news content
if st.session_state.news_data:
    # Check if translation is needed
    if selected_language != "English" and st.session_state.sutra_api_key:
        with st.spinner(f"Translating news to {selected_language}..."):
            translated_news = translate_news(
                st.session_state.news_data, 
                selected_language,
                st.session_state.sutra_api_key
            )
    else:
        # Display English news (or show message if Sutra API key is missing)
        if selected_language != "English" and not st.session_state.sutra_api_key:
            st.warning("Please enter your Sutra API key in the sidebar to translate news.")
        
        # Format and display the original news with improved layout
        news_container = st.container()
        for i, news in enumerate(st.session_state.news_data):
            with news_container:
                # Create two columns with adjusted ratio
                col1, col2 = st.columns([3, 2])
                
                # Left column for text content
                with col1:
                    st.markdown(f"### {i+1}. {news.get('title', 'No Title')}")
                    st.markdown(f"**Source:** {news.get('source', 'Unknown')} | {news.get('date', 'Unknown date')}")
                    st.markdown(news.get('snippet', 'No description available.'))
                    st.markdown(f"[Read more]({news.get('link', '#')})")
                
                # Right column for image with fixed height
                with col2:
                    if news.get('imageUrl'):
                        # Add custom CSS for image container
                        st.markdown("""
                            <style>
                            .image-container {
                                height: 200px;
                                overflow: hidden;
                                border-radius: 10px;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            }
                            .image-container img {
                                width: 100%;
                                height: 100%;
                                object-fit: cover;
                            }
                            </style>
                            """, unsafe_allow_html=True)
                        
                        # Wrap image in styled container
                        st.markdown(f"""
                            <div class="image-container">
                                <img src="{news.get('imageUrl')}" alt="News Image">
                            </div>
                            """, unsafe_allow_html=True)
                
                st.divider()
else:
    if not st.session_state.serper_api_key:
        st.info("Enter your Serper API key and search for news to get started.")
    else:
        st.info("No news data available. Try searching for a topic.")