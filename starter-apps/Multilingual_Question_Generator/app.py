import streamlit as st
from educhain import Educhain, LLMConfig
from educhain.engines import qna_engine
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables if available
load_dotenv()

# Set page configuration at the very top of the script
st.set_page_config(page_title="Multilingual Question Generator", page_icon="🌐", layout="wide")

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

# Define question types
question_types = ["Multiple Choice", "Short Answer", "True/False", "Fill in the Blank"]

# --- Sidebar Configuration ---
with st.sidebar:
    st.sidebar.image("https://framerusercontent.com/images/T5kFJeyNUyAYJBz4PaWuP7Bfr0.png", use_container_width=True)
    st.header("⚙️ Configuration")
    
    # Use environment variable if available, otherwise hide API key input
    api_key = os.getenv("SUTRA_API_KEY", "")
    if not api_key:
        api_key = st.text_input("Sutra API Key", value="", type="password")
        if not api_key:
            st.warning("Please set your Sutra API Key as an environment variable or enter it above")
    
    # Question type selection
    selected_question_type = st.selectbox("Question Type:", question_types)
    
    # Language selection
    selected_language = st.selectbox("Language for questions:", languages)
    
    # Number of questions
    num_questions = st.slider("Number of Questions", 1, 8, 3)
    
    st.markdown("---")
    st.markdown("**Powered by** [Educhain](https://github.com/satvik314/educhain)")
    st.markdown("**Using** [Sutra LLM](https://docs.two.ai/) for multilingual")
    st.write("❤️ Built with [Streamlit](https://streamlit.io)")

# --- Initialize Educhain with Sutra Model ---
@st.cache_resource
def initialize_educhain(api_key):
    if not api_key:
        return None  # Return None if API key is missing

    sutra_model = ChatOpenAI(
        api_key=api_key,
        base_url="https://api.two.ai/v2",
        model="sutra-v2",
        temperature=0.9
    )
    llm_config = LLMConfig(custom_model=sutra_model)
    return Educhain(llm_config)

# --- Utility Function to Display Questions ---
def display_questions(questions, language):
    if questions and hasattr(questions, "questions"):
        st.success(f"Generated {len(questions.questions)} questions in {language}")
        
        for i, question in enumerate(questions.questions):
            st.subheader(f"Question {i + 1}:")

            if hasattr(question, 'options'):  # Multiple Choice
                st.write(f"**Question:** {question.question}")
                st.write("**Options:**")
                for j, option in enumerate(question.options):
                    st.write(f"   {chr(65 + j)}. {option}")
                if hasattr(question, 'answer'):
                    st.write(f"**Correct Answer:** {question.answer}")
                if hasattr(question, 'explanation') and question.explanation:
                    st.write(f"**Explanation:** {question.explanation}")

            else:  # Short Answer, True/False, Fill in the Blank
                st.write(f"**Question:** {question.question}")
                if hasattr(question, 'answer'):
                    st.write(f"**Answer:** {question.answer}")
                if hasattr(question, 'explanation') and question.explanation:
                    st.write(f"**Explanation:** {question.explanation}")
                if hasattr(question, 'keywords') and question.keywords:  # Display keywords if present
                    st.write(f"**Keywords:** {', '.join(question.keywords)}")

            st.markdown("---")

# Function to add language instruction to custom instructions
def add_language_instruction(custom_instr, language):
    lang_instruction = f"Generate all questions, options, answers and explanations in {language} language."
    if custom_instr:
        return f"{lang_instruction} {custom_instr}"
    return lang_instruction

# --- Streamlit App Layout ---
st.markdown(
    f'<h1><img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png" width="60"/> Multilingual Question Generator </h1>',
    unsafe_allow_html=True
    )
st.markdown(f"Generate {selected_question_type} questions in **{selected_language}** using Sutra LLM and Educhain")

# --- Initialize Educhain client if API key is provided ---
if api_key:
    educhain_client = initialize_educhain(api_key)
    if educhain_client:
        qna_engine = educhain_client.qna_engine
    else:
        st.error("Failed to initialize Educhain. Please check your Sutra API key.")
        st.stop()
else:
    st.warning("Please enter your Sutra API Key in the sidebar or set it as an environment variable to continue.")
    st.stop()

# --- Main Content Area ---
default_topics = {
    "Multiple Choice": "Science",
    "Short Answer": "History", 
    "True/False": "Geography",
    "Fill in the Blank": "Math"
}

topic = st.text_input("Enter Topic:", default_topics.get(selected_question_type, "Science"))
custom_instructions = st.text_area(
    "Custom Instructions (optional):", 
    placeholder=f"e.g. 'Focus on advanced concepts for {selected_question_type} questions'",
    height=100
)

# Update custom instructions with language requirement
language_custom_instructions = add_language_instruction(custom_instructions, selected_language)

# Generate button
if st.button("Generate Questions"):
    with st.spinner(f"Generating {num_questions} {selected_question_type.lower()} questions in {selected_language}..."):
        questions = qna_engine.generate_questions(
            topic=topic,
            num=num_questions,
            question_type=selected_question_type,
            custom_instructions=language_custom_instructions
        )
        display_questions(questions, selected_language)
