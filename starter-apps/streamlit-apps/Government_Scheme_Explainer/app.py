import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("SUTRA_API_KEY")

# Page configuration
st.set_page_config(
    page_title="Government Scheme Explainer",
    page_icon="🏛️",
    layout="wide"
)

# Define supported languages with native script names
languages = [
    "English", 
    "Hindi (हिन्दी)", 
    "Gujarati (ગુજરાતી)", 
    "Bengali (বাংলা)", 
    "Tamil (தமிழ்)", 
    "Telugu (తెలుగు)", 
    "Kannada (ಕನ್ನಡ)", 
    "Malayalam (മലയാളം)", 
    "Punjabi (ਪੰਜਾਬੀ)", 
    "Marathi (मराठी)", 
    "Urdu (اردو)",
    "Assamese (অসমীয়া)", 
    "Odia (ଓଡ଼ିଆ)"
]

# Define government scheme categories with schemes
govt_schemes = {
    "👨‍🌾 Agriculture & Rural": [
        "PM-KISAN",
        "Kisan Credit Card",
        "Soil Health Card",
        "MGNREGA",
        "National Rural Livelihood Mission"
    ],
    "🏠 Housing & Urban": [
        "Pradhan Mantri Awas Yojana (PMAY)",
        "Smart Cities Mission",
        "AMRUT",
        "Housing for All",
        "Swachh Bharat Mission"
    ],
    "🏥 Health & Wellness": [
        "Ayushman Bharat",
        "PM Jan Arogya Yojana",
        "National Health Mission",
        "Pradhan Mantri Surakshit Matritva Abhiyan",
        "Mission Indradhanush"
    ],
    "👩‍🎓 Education & Skills": [
        "Samagra Shiksha",
        "PM POSHAN (Mid Day Meal)",
        "Skill India Mission",
        "National Education Policy",
        "PM Vidya Scheme"
    ],
    "💼 Employment & Entrepreneurship": [
        "PM Mudra Yojana",
        "Startup India",
        "Stand Up India",
        "Pradhan Mantri Rozgar Protsahan Yojana",
        "Deen Dayal Upadhyaya Grameen Kaushalya Yojana"
    ],
    "👵 Social Security & Pension": [
        "Atal Pension Yojana",
        "PM Vaya Vandana Yojana",
        "National Social Assistance Programme",
        "PM Jeevan Jyoti Bima Yojana",
        "PM Suraksha Bima Yojana"
    ],
    "💡 Energy & Infrastructure": [
        "Saubhagya (Electricity for All)",
        "Ujjwala Yojana",
        "National Solar Mission",
        "PM Gram Sadak Yojana",
        "Bharatmala Pariyojana"
    ],
    "🏦 Financial Inclusion": [
        "Jan Dhan Yojana",
        "Sukanya Samriddhi Yojana",
        "PM Garib Kalyan Yojana",
        "Digital India",
        "BHIM UPI"
    ]
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

# Custom CSS for better dark mode support
st.markdown("""
    <style>
    .scheme-card {
        background-color: rgba(25, 118, 210, 0.1);
        border: 1px solid #1976D2;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .scheme-title {
        color: #1976D2;
        font-weight: bold;
        font-size: 1.2em;
    }
    .light-text {
        color: #FFFFFF;
    }
    .highlight-box {
        background-color: rgba(25, 118, 210, 0.1);
        border: 1px solid #1976D2;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for scheme selection and options
st.sidebar.image("https://i.pinimg.com/736x/15/9f/48/159f48b6cc504550eda56fe698eb3324.jpg", use_container_width=True)
with st.sidebar:
    st.subheader("🏛️ GOV Scheme Explainer")
    
    # Language selector with native scripts
    selected_language = st.selectbox("Select language / भाषा चुनें:", languages)
    
    # Extract just the language name without the script
    selected_language_simple = selected_language.split(" ")[0]
    
    # Main category selector
    selected_main_category = st.selectbox(
        "Select Sector / क्षेत्र चुनें:",
        options=list(govt_schemes.keys())
    )
    
    # Scheme selector based on main category
    selected_scheme = st.selectbox(
        "Select Scheme / योजना चुनें:",
        options=govt_schemes[selected_main_category]
    )
    
    
    
    # Explanation focus options
    with st.expander("Explanation Focus / व्याख्या फोकस", expanded=False):
        benefits_focus = st.slider(
            "Benefits explanation / लाभ व्याख्या",
            min_value=1,
            max_value=5,
            value=4,
            help="1: Brief, 5: Detailed benefits"
        )
        
        eligibility_focus = st.slider(
            "Eligibility details / पात्रता विवरण",
            min_value=1,
            max_value=5,
            value=4,
            help="1: Brief, 5: Detailed eligibility"
        )
        
        application_focus = st.slider(
            "Application process / आवेदन प्रक्रिया",
            min_value=1,
            max_value=5,
            value=3,
            help="1: Brief, 5: Detailed application steps"
        )
        
        include_examples = st.checkbox(
            "Include examples / उदाहरण शामिल करें",
            value=True
        )
        
        include_comparison = st.checkbox(
            "Compare to similar schemes / समान योजनाओं से तुलना करें",
            value=False
        )
    
    # User persona for tailored explanations
    with st.expander("User Persona / उपयोगकर्ता प्रोफाइल", expanded=False):
        user_education = st.select_slider(
            "Education Level / शिक्षा स्तर",
            options=["Basic", "Intermediate", "Advanced"],
            value="Intermediate"
        )
        
        user_familiarity = st.select_slider(
            "Government Scheme Familiarity / सरकारी योजना परिचितता",
            options=["Low", "Medium", "High"],
            value="Medium"
        )
        
        user_location = st.selectbox(
            "Location Type / स्थान प्रकार",
            options=["Rural", "Urban", "Semi-urban"],
            index=0  # Default to first option (Rural)
        )
    
   
    
    # Show current selections in colored box
    st.markdown(
        f"""
        <div class="highlight-box">
            <p class="light-text">🗣️ <b>Language:</b> {selected_language}</p>
            <p class="light-text">📋 <b>Scheme:</b> {selected_scheme}</p>
            <p class="light-text">👤 <b>User profile:</b> {user_education} education, {user_familiarity} familiarity</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Main content
st.markdown(
    f'<h1 style="color: #1976D2;"><img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png" width="55"/> Government Scheme Explainer 🏛️</h1>',
    unsafe_allow_html=True
    )


# Initialize session state for messages and selected scheme
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_scheme" not in st.session_state:
    st.session_state.last_scheme = None

# Check if scheme changed - no question buttons anymore
if st.session_state.last_scheme != selected_scheme:
    st.session_state.last_scheme = selected_scheme
    # We've removed the question buttons from here

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input with dynamic placeholder based on selected category
chat_placeholder = f"Ask about {selected_scheme}..."
user_input = st.chat_input(chat_placeholder)

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
            
            # Create system message for the government scheme explainer
            system_message = f"""You are a Government Scheme Explainer, specializing in explaining Indian government schemes in simple terms.
            
            The user wants to know about: {selected_scheme} (Category: {selected_main_category}).
            
            Focus areas for your explanation:
            - Benefits explanation: {'Detailed' if benefits_focus >= 4 else 'Moderate' if benefits_focus >= 2 else 'Brief'}
            - Eligibility details: {'Detailed' if eligibility_focus >= 4 else 'Moderate' if eligibility_focus >= 2 else 'Brief'}
            - Application process: {'Detailed' if application_focus >= 4 else 'Moderate' if application_focus >= 2 else 'Brief'}
            - {'Include practical examples and case studies.' if include_examples else 'Avoid examples and focus on core information.'}
            - {'Compare this scheme with similar schemes to highlight differences.' if include_comparison else 'Focus only on this scheme without comparisons.'}
            
            User profile:
            - Education level: {user_education}
            - Familiarity with government schemes: {user_familiarity}
            - Location type: {user_location}
            
            Adjust your explanation complexity based on this profile.
            
            Format your response clearly with:
            - Short paragraphs
            - Bullet points for lists
            - Bold text for important information
            - Section headings if the response is long
            
            Please respond in {selected_language_simple}.
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
            st.error("Please check your Sutra API key in the environment variables.")
