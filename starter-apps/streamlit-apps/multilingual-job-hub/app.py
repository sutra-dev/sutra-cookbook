import streamlit as st
import requests
import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.callbacks.base import BaseCallbackHandler

# Try importing SerpAPI, show error if not installed
try:
    from serpapi import GoogleSearch
except ImportError:
    st.error("""
    The required package 'google-search-results' is not installed. 
    Please install it using:
    ```
    pip install google-search-results
    ```
    """)
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Multilingual Job Hub",
    page_icon="💼",
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

# Function to fetch jobs using SerpAPI
def fetch_jobs(query, num_results=20, location="Worldwide", job_type=None):
    # First fetch jobs
    params = {
        "api_key": st.session_state.serp_api_key,
        "engine": "google_jobs",
        "q": query,
        "google_domain": "google.com",
        "hl": "en",
        "gl": "in",
        "location": location,
        "ltype": "1"  # Full-time jobs
    }
    
    if job_type:
        params["q"] = f"{query} {job_type}"
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        jobs = results.get("jobs_results", [])
        
        # Limit the number of jobs
        jobs = jobs[:num_results]
        
        # Enhance jobs with high-quality company logos
        enhanced_jobs = []
        for job in jobs:
            company_name = job.get('company_name', '')
            if company_name:
                # Fetch company logo using Google Images
                image_params = {
                    "api_key": st.session_state.serp_api_key,
                    "engine": "google_images",
                    "q": f"{company_name} company logo",
                    "num": 1,  # We only need one image
                    "safe": "active",
                    "tbm": "isch"  # Image search
                }
                
                try:
                    image_search = GoogleSearch(image_params)
                    image_results = image_search.get_dict()
                    if image_results.get("images_results") and len(image_results["images_results"]) > 0:
                        # Get the highest quality image URL
                        image_url = image_results["images_results"][0].get("original")
                        if image_url:
                            job['thumbnail'] = image_url
                except Exception as e:
                    st.warning(f"Error fetching logo for {company_name}: {str(e)}")
            
            enhanced_jobs.append(job)
        
        return enhanced_jobs
    except Exception as e:
        st.error(f"Error fetching jobs: {str(e)}")
        return []

# Function to translate jobs using Sutra LLM
def translate_jobs(jobs, target_language, api_key):
    try:
        # Get base model (non-streaming) for translation
        model = get_base_chat_model(api_key)
        
        # Create a container for all jobs
        jobs_container = st.container()
        
        # Process each job individually
        translated_items = []
        for i, job in enumerate(jobs):
            # Create a specific prompt for each job
            system_message = f"""
            You are a professional translator specializing in job listings translation. Translate the following job content to {target_language}.
            
            Translation Rules:
            1. Translate ONLY these fields:
               - title: Keep it concise and job-focused
               - company_name: Translate the company name if it has a common translation
               - description: Maintain the job requirements and responsibilities context
               - location: Translate location information
            
            2. Translation Guidelines:
               - Ensure natural and fluent language
               - Maintain the original meaning and context
               - Keep any technical terms, skills, and requirements in their original form
               - Preserve any numbers, dates, and measurements
               - Keep any job-specific terminology accurate
            
            3. Return ONLY the translated fields in this exact format:
            {{
                "title": "translated title",
                "company_name": "translated company name",
                "description": "translated description",
                "location": "translated location"
            }}
            
            4. Important:
               - Do not add any explanations
               - Do not modify the JSON structure
               - Do not translate any other fields
               - Ensure the translation is culturally appropriate for {target_language} speakers
            """
            
            # Prepare only the fields that need translation
            fields_to_translate = {
                "title": job.get('title', ''),
                "company_name": job.get('company_name', ''),
                "description": job.get('description', '')[:500], # Truncate description before sending for translation
                "location": job.get('location', '')
            }
            
            # Convert to JSON string
            job_json = json.dumps(fields_to_translate, ensure_ascii=False)
            
            # Generate response
            messages = [
                HumanMessage(content=f"{system_message}\n\nFields to translate:\n{job_json}")
            ]
            
            try:
                # Show processing status
                with st.spinner(f"Translating job {i+1} of {len(jobs)}..."):
                    response = model.invoke(messages)
                    result = response.content.strip()
                    
                    # Clean the response
                    result = result.replace('```json', '').replace('```', '').strip()
                    
                    # Parse the translated fields
                    translated_fields = json.loads(result)
                    
                    # Create new item with translated fields and original data
                    translated_job = {
                        **job,  # Keep all original fields
                        "title": translated_fields.get('title', job.get('title', '')),
                        "company_name": translated_fields.get('company_name', job.get('company_name', '')),
                        "description": translated_fields.get('description', job.get('description', '')),
                        "location": translated_fields.get('location', job.get('location', ''))
                    }
                    
                    translated_items.append(translated_job)
                    
                    # Display the translated job with improved layout
                    with jobs_container:
                        st.markdown(f"""
                            <div class="job-card">
                                <div style="display: flex; gap: 20px;">
                                    <div style="flex: 3;">
                                        <h3 class="job-title">{i+1}. {translated_job['title']}</h3>
                                        <p class="company-name">🏢 <strong>Company:</strong> {translated_job['company_name']}</p>
                                        <p class="job-location">📍 <strong>Location:</strong> {translated_job['location']}</p>
                                        <p class="job-type">⏰ <strong>Type:</strong> {translated_job.get('detected_extensions', {}).get('schedule_type', 'Not specified')}</p>
                                        <p class="job-description">{translated_job['description'][:300]}...</p>
                                        <p><a href="{translated_job.get('share_link', '#')}" class="job-link" target="_blank">🔗 View Job</a></p>
                                    </div>
                                    <div style="flex: 1;">
                                        {f'<div class="image-container"><img src="{translated_job.get("thumbnail")}" alt="Company Logo"></div>' if translated_job.get('thumbnail') else ''}
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            except json.JSONDecodeError as e:
                st.warning(f"Failed to parse translation of job {i+1}: {str(e)}. Using original.")
                translated_items.append(job)
            except Exception as e:
                st.warning(f"Error translating job {i+1}: {str(e)}. Using original.")
                translated_items.append(job)
        
        return translated_items
            
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return jobs

# Function to translate search query to English using Sutra LLM
def translate_query_to_english(query, api_key):
    try:
        # Get base model (non-streaming) for translation
        model = get_base_chat_model(api_key)
        
        system_message = """
        You are a professional translator specializing in job search queries. Translate the following search query to English.
        
        Translation Rules:
        1. Keep the translation concise and clear
        2. Maintain the search intent and job-related terminology
        3. Preserve any proper nouns (names, places)
        4. Keep any numbers, dates, and measurements
        5. Ensure the translation is natural and search-friendly
        6. For technical terms (like "Full Stack", "Developer", etc.), use standard English terminology
        7. If the query is already in English, return it as is
        
        Return ONLY the translated query without any explanations or additional text.
        """
        
        messages = [
            HumanMessage(content=f"{system_message}\n\nQuery to translate:\n{query}")
        ]
        
        response = model.invoke(messages)
        translated_query = response.content.strip()
        
        # Log the translation for debugging
        st.write(f"Debug - Original query: {query}")
        st.write(f"Debug - Translated query: {translated_query}")
        
        return translated_query
        
    except Exception as e:
        st.error(f"Error translating query: {str(e)}")
        st.warning("Using original query as fallback.")
        return query

# Initialize session state variables
if "serp_api_key" not in st.session_state:
    st.session_state.serp_api_key = ""
if "sutra_api_key" not in st.session_state:
    st.session_state.sutra_api_key = ""
if "jobs_data" not in st.session_state:
    st.session_state.jobs_data = []
if "search_query" not in st.session_state:
    st.session_state.search_query = "GenAI Engineering"
if "num_results" not in st.session_state:
    st.session_state.num_results = 20  # Default value

# Sidebar for settings
with st.sidebar:
    st.markdown(
        f'<h1>💼 Job Hub</h1>',
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
    
    st.markdown("**SerpAPI**")
    st.markdown("Get your API key from [SerpAPI](https://serpapi.com/users/sign_in)")
    serp_api_key = st.text_input("Enter your SerpAPI Key:", 
                                value=st.session_state.serp_api_key,
                                type="password",
                                label_visibility="collapsed")
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
    
    location = st.selectbox("Location:", 
                           ["India", "Mexico", "Japan", "Germany", "France", "Brazil", "Indonesia"])
    
    # Language selector
    st.markdown("### Language Settings")
    selected_language = st.selectbox("Select language:", languages)
    
    st.divider()
    st.markdown(f"Currently viewing jobs in: **{selected_language}**")
    
    # About section
    with st.expander("About Job Hub"):
        st.markdown("""
        This app uses:
        - **SerpAPI** to fetch job listings from around the world
        - **Sutra LLM** to translate job details into 50+ languages
        - **Streamlit** for the interactive web interface
        
        Search for any job and get details in your preferred language!
        """)

# Main content area
st.markdown(
    f'<h1><img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png" width="60" style="vertical-align: middle;"/> Multilingual Job Search<img src="https://pixcap.com/cdn/library/templates/0bb47b92-ac86-457c-99c6-e05a7c0cf4e3/thumbnail/f7ff3dee-c635-43aa-82bf-596fae43744f_transparent_null_400.webp" width="90" height="90" style="vertical-align: middle;"/></h1>',
    unsafe_allow_html=True
)

# Search bar
col1, col2 = st.columns([4, 1])
with col1:
    search_query = st.text_input("Search for jobs:", value=st.session_state.search_query)
with col2:
    search_button = st.button("Search", type="primary", use_container_width=True)

# Validate API keys before searching
if search_button or (not st.session_state.jobs_data and st.session_state.serp_api_key):
    if not st.session_state.serp_api_key:
        st.error("Please enter your SerpAPI key in the sidebar.")
    else:
        st.session_state.search_query = search_query
        
        # Translate query to English if needed
        if selected_language != "English" and st.session_state.sutra_api_key:
            with st.spinner("Translating search query to English..."):
                english_query = translate_query_to_english(search_query, st.session_state.sutra_api_key)
                if english_query != search_query:  # Only show if translation actually happened
                    st.info(f"Translated query: '{english_query}'")
        else:
            english_query = search_query
        
        # Show loading message
        with st.spinner(f"Fetching jobs for '{english_query}'..."):
            # Fetch jobs data
            jobs = fetch_jobs(
                query=english_query,
                location=location if location != "Worldwide" else None # Use selected location, or None for worldwide
            )
            
            if jobs:
                st.session_state.jobs_data = jobs
                st.success(f"Found {len(jobs)} jobs!")
            else:
                st.warning("No jobs found. Try a different search term.")

# Display jobs content
if st.session_state.jobs_data:
    # Check if translation is needed
    if selected_language != "English" and st.session_state.sutra_api_key:
        with st.spinner(f"Translating jobs to {selected_language}..."):
            translated_jobs = translate_jobs(
                st.session_state.jobs_data, 
                selected_language,
                st.session_state.sutra_api_key
            )
    else:
        # Display English jobs (or show message if Sutra API key is missing)
        if selected_language != "English" and not st.session_state.sutra_api_key:
            st.warning("Please enter your Sutra API key in the sidebar to translate jobs.")
        
        # Format and display the original jobs with improved layout
        jobs_container = st.container()
        for i, job in enumerate(st.session_state.jobs_data):
            st.markdown(f"""
                <div class="job-card">
                    <div style="display: flex; gap: 20px;">
                        <div style="flex: 3;">
                            <h3 class="job-title">{i+1}. {job.get('title', 'No Title')}</h3>
                            <p class="company-name">🏢 <strong>Company:</strong> {job.get('company_name', 'Unknown')}</p>
                            <p class="job-location">📍 <strong>Location:</strong> {job.get('location', 'Location not specified')}</p>
                            <p class="job-type">⏰ <strong>Type:</strong> {job.get('detected_extensions', {}).get('schedule_type', 'Not specified')}</p>
                            <p class="job-description">{job.get('description', 'No description available.')[:300]}...</p>
                            <p><a href="{job.get('share_link', '#')}" class="job-link" target="_blank">🔗 View Job</a></p>
                        </div>
                        <div style="flex: 1;">
                            {f'<div class="image-container"><img src="{job.get("thumbnail")}" alt="Company Logo"></div>' if job.get('thumbnail') else ''}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    if not st.session_state.serp_api_key:
        st.info("Enter your SerpAPI key and search for jobs to get started.")
    else:
        st.info("No job data available. Try searching for a job.")

# Add custom CSS for job cards
st.markdown("""
    <style>
    /* Theme-aware styles */
    .job-card {
        background-color: var(--background-color);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid var(--border-color);
    }
    .job-title {
        color: var(--text-color);
        font-size: 1.5em;
        margin-bottom: 10px;
    }
    .company-name {
        color: var(--text-color-secondary);
        font-size: 1.1em;
        margin: 5px 0;
    }
    .job-location {
        color: var(--text-color-secondary);
        font-size: 1.1em;
        margin: 5px 0;
    }
    .job-type {
        color: var(--accent-color);
        font-size: 1.1em;
        margin: 5px 0;
    }
    .job-description {
        color: var(--text-color-secondary);
        font-size: 1em;
        margin: 10px 0;
        line-height: 1.5;
    }
    .job-link {
        color: var(--link-color);
        text-decoration: none;
        font-weight: bold;
    }
    .job-link:hover {
        color: var(--link-hover-color);
        text-decoration: underline;
    }
    .image-container {
        height: 150px;  /* Increased height for better visibility */
        overflow: hidden;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid var(--border-color);
        background-color: white;  /* White background for logos */
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 10px;
    }
    .image-container img {
        width: 100%;
        height: 100%;
        object-fit: contain;  /* Changed to contain for better logo display */
        max-width: 100%;
        max-height: 100%;
    }

    /* Light theme variables */
    [data-theme="light"] {
        --background-color: #ffffff;
        --text-color: #1f1f1f;
        --text-color-secondary: #4a4a4a;
        --border-color: #e0e0e0;
        --accent-color: #2e7d32;
        --link-color: #1565c0;
        --link-hover-color: #0d47a1;
    }

    /* Dark theme variables */
    [data-theme="dark"] {
        --background-color: #262730;
        --text-color: #ffffff;
        --text-color-secondary: #e0e0e0;
        --border-color: #3e3e3e;
        --accent-color: #4caf50;
        --link-color: #90caf9;
        --link-hover-color: #42a5f5;
    }

    /* Additional theme-aware improvements */
    .stMarkdown {
        color: var(--text-color);
    }
    .stMarkdown strong {
        color: var(--text-color);
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--text-color);
    }
    .stMarkdown a {
        color: var(--link-color);
    }
    .stMarkdown a:hover {
        color: var(--link-hover-color);
    }

    /* Ensure proper contrast for all text elements */
    .stTextInput > div > div > input {
        color: var(--text-color);
        background-color: var(--background-color);
    }
    .stSelectbox > div > div > select {
        color: var(--text-color);
        background-color: var(--background-color);
    }
    .stSlider > div > div > div {
        color: var(--text-color);
    }
    </style>
    """, unsafe_allow_html=True) 