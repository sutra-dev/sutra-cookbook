import streamlit as st
from typing import Optional, List, Type, Any
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
import os
from dotenv import load_dotenv
load_dotenv()

# Set page configuration
st.set_page_config(page_title="Multilingual Flashcard Generator", page_icon="🌐", layout="wide")

# Define supported languages
languages = [
    "English", "Hindi", "Gujarati", "Bengali", "Tamil", 
    "Telugu", "Kannada", "Malayalam", "Punjabi", "Marathi", 
    "Urdu", "Assamese", "Sanskrit", "Korean", 
    "Japanese", "Arabic", "French", "German", "Spanish", 
    "Portuguese", "Russian", "Chinese", "Vietnamese", "Thai", 
    "Indonesian", "Turkish", "Polish", "Ukrainian", "Dutch", 
    "Italian", "Greek", "Hebrew", "Persian", "Swedish", 
    "Norwegian", "Danish", "Finnish", "Czech", "Hungarian", 
    "Romanian", "Bulgarian", "Croatian", "Serbian", "Slovak", 
    "Slovenian", "Estonian", "Latvian", "Lithuanian", "Malay", 
    "Tagalog", "Swahili"
]

class LLMConfig:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "sutra-v2",
        max_tokens: int = 1500,
        temperature: float = 0.7,
        custom_model: Optional[Any] = None,
        base_url: Optional[str] = "https://api.two.ai/v2",
        default_headers: Optional[dict] = None
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.custom_model = custom_model
        self.base_url = base_url
        self.default_headers = default_headers

class Flashcard(BaseModel):
    front: str = Field(..., description="The front side of the flashcard with a question or key term")
    back: str = Field(..., description="The back side of the flashcard with the answer or definition")
    explanation: Optional[str] = Field(None, description="An optional explanation or additional context")

class FlashcardSet(BaseModel):
    title: str = Field(..., description="The title or topic of the flashcard set")
    flashcards: List[Flashcard] = Field(..., description="A list of flashcards in this set")

class ContentEngine:
    def __init__(self, llm_config: Optional[LLMConfig] = None):
        if llm_config is None:
            llm_config = LLMConfig()
        self.llm = self._initialize_llm(llm_config)

    def _initialize_llm(self, llm_config: LLMConfig):
        if llm_config.custom_model:
            return llm_config.custom_model
        else:
            return ChatOpenAI(
                model=llm_config.model_name,
                api_key=llm_config.api_key,
                max_tokens=llm_config.max_tokens,
                temperature=llm_config.temperature,
                base_url=llm_config.base_url,
                default_headers=llm_config.default_headers
            )
    
    def generate_flashcards(
        self,
        topic: str,
        language: str = "English",
        num: int = 10,
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        llm: Optional[Any] = None,
        **kwargs
    ) -> FlashcardSet:
        if response_model is None:
            response_model = FlashcardSet
        parser = PydanticOutputParser(pydantic_object=response_model)
        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = """
            You are an expert educational content creator specializing in creating high-quality, professional flashcards that meet industry standards. Your task is to generate a set of {num} exceptional flashcards on the topic: {topic}.
            
            IMPORTANT: Generate all content in {language} language with perfect grammar and natural phrasing as if written by a native speaker.

            Follow these guidelines to create professional-grade flashcards:

            1. FRONT SIDE:
               - Create clear, concise, and precisely worded questions or key terms
               - For terminology cards: use the exact technical term, properly formatted and spelled
               - For concept cards: phrase as a specific question that targets one discrete concept
               - For problem-solving cards: present a clear, solvable problem
               - Ensure appropriate complexity level for the target subject
               - Use proper notation, symbols, and formatting when applicable

            2. BACK SIDE:
               - Provide complete yet concise answers that directly address the front side
               - Include the essential information without unnecessary verbosity
               - For definitions: provide accurate, authoritative definitions from the field
               - For problem solutions: show the complete answer with critical steps
               - Use bullet points for multi-part answers when appropriate
               - Maintain academic accuracy and precision

            3. EXPLANATION:
               - Provide valuable additional context that enhances understanding
               - Include examples, applications, or memory aids when helpful
               - Mention connections to other concepts in the field
               - Add relevant details that aid deeper comprehension
               - For difficult concepts, provide alternative explanations
               - Include mnemonics, visual cues, or learning strategies when appropriate

            Create a balanced set covering:
            - Foundational concepts (30%)
            - Key terminology (30%)
            - Important processes or procedures (20%)
            - Advanced applications or edge cases (20%)

            The flashcards should progress from fundamental to more complex concepts in a logical learning sequence.

            Ensure that the output follows this structure:
            - A descriptive and specific title for the flashcard set
            - A list of flashcards, each containing:
              - front: The question or key term (concise and clear)
              - back: The answer or definition (complete but focused)
              - explanation: Enhanced context with examples or applications
            """

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        prompt_template += "\n\nThe response should be in JSON format.\n{format_instructions}"

        flashcard_prompt = PromptTemplate(
            input_variables=["num", "topic", "language"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        llm_to_use = llm if llm is not None else self.llm
        flashcard_chain = flashcard_prompt | llm_to_use
        results = flashcard_chain.invoke(
            {"num": num, "topic": topic, "language": language, **kwargs},
        )

        try:
            structured_output = parser.parse(results.content)
            return structured_output
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:")
            print(results.content)
            return FlashcardSet(title=topic, flashcards=[])

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Use environment variable if available, otherwise hide API key input
    api_key = os.getenv("SUTRA_API_KEY", "")
    if not api_key:
        api_key = st.text_input("Sutra API Key", value="", type="password")
        if not api_key:
            st.warning("Please set your Sutra API Key as an environment variable or enter it above")
    
    # Language selection
    selected_language = st.selectbox("Language for flashcards:", languages)
    
    # Number of flashcards
    num_cards = st.slider("Number of Flashcards", 1, 8, 3)
    
    # Custom instructions
    custom_instructions = st.text_area(
        "Custom Instructions (optional):", 
        placeholder=f"e.g., 'Focus on advanced concepts' or 'Include examples'",
        height=100
    )
    
    st.markdown("---")
    st.markdown("**Powered by** [Educhain](https://github.com/satvik314/educhain)")
    st.markdown("**Using** [Sutra LLM](https://twoai.com/) for multilingual generation")
    st.write("❤️ Built with [Streamlit](https://streamlit.io)")

# Initialize ContentEngine with Sutra LLM if API key is provided
if api_key:
    llm_config = LLMConfig(api_key=api_key)
    content_engine = ContentEngine(llm_config)

# --- Main UI ---
# Main header
st.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <h1><img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png" width="60"/> Professional Flashcard Studio</h1>
    <p style="font-size: 1.2rem;">Create industry-standard educational flashcards powered by TWO AI</p>
</div>
""", unsafe_allow_html=True)


# Language indicator
st.markdown(f"""
<div style="padding: 0.75rem; border-radius: 6px; margin-bottom: 1.5rem;">
    <span style="font-size: 1.25rem; margin-right: 8px;">🔤</span>
    <span>Currently generating content in <strong>{selected_language}</strong></span>
</div>
""", unsafe_allow_html=True)

# Check if API key is available
if not api_key:
    st.warning("Please enter your Sutra API Key in the sidebar or set it as an environment variable to continue.")
    st.stop()

# Topic input
topic = st.text_input(
    "📝 What topic would you like flashcards for?",
    placeholder=f"e.g., Quantum Physics, Machine Learning, World History, etc.",
    help=f"Enter any educational topic to generate professional flashcards in {selected_language}"
)

# Use custom instructions directly
full_instructions = custom_instructions if custom_instructions else ""

# Generate button
if st.button("🚀 Generate Professional Flashcards", type="primary", use_container_width=True):
    if topic:
        with st.spinner(f"🧠 Generating {num_cards} flashcards in {selected_language}..."):
            flashcard_set = content_engine.generate_flashcards(
                topic=topic,
                language=selected_language,
                num=num_cards,
                custom_instructions=full_instructions
            )
        
        # Success message without background colors
        st.markdown(f"""
        <div style="padding: 1rem; margin: 1.5rem 0; border: 1px solid;">
            <h3 style="margin-top: 0; font-size: 1.25rem;">✅ Flashcards Successfully Generated</h3>
            <p style="margin-bottom: 0;">Created {len(flashcard_set.flashcards)} professional flashcards on <strong>{flashcard_set.title}</strong> in {selected_language}</p>
        </div>
        
        <div style="padding: 1rem; margin-bottom: 2rem; border: 1px solid;">
            <h4 style="margin-top: 0;">Studying Tips:</h4>
            <ul>
                <li>Review cards regularly using spaced repetition</li>
                <li>Test yourself by trying to recall before viewing the answer</li>
                <li>Connect new concepts with what you already know</li>
                <li>Study in short, focused sessions rather than long marathons</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Display flashcards in a single column with minimal styling
        st.markdown("""
        <style>
        .flashcard-container {
            margin-bottom: 1.5rem;
        }
        .flashcard {
            border: 1px solid;
            border-radius: 8px;
            overflow: hidden;
        }
        .flashcard-front {
            padding: 1.5rem;
            border-bottom: 1px solid;
        }
        .flashcard-back {
            padding: 1.5rem;
        }
        .flashcard-explanation {
            padding: 1rem 1.5rem;
            border-top: 1px solid;
            font-size: 0.9rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display flashcards in a single column
        for i, flashcard in enumerate(flashcard_set.flashcards, 1):
            with st.expander(f"**Flashcard {i}**", expanded=False):
                st.markdown(f"""
                <div class="flashcard-container">
                    <div class="flashcard">
                        <div class="flashcard-front">
                            <h3 style="margin-top:0;">{flashcard.front}</h3>
                        </div>
                        <div class="flashcard-back">
                            <p style="margin-bottom:0;">{flashcard.back}</p>
                        </div>
                        {f'<div class="flashcard-explanation"><p style="margin:0;"><strong>💡 Explanation:</strong> {flashcard.explanation}</p></div>' if flashcard.explanation else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a topic for the flashcards.")

# Footer
st.markdown("---")
st.markdown("""
**Note:** This application uses the Sutra LLM to generate flashcards in multiple languages. 
The quality of translations and content generation may vary by language.
""")

st.markdown(
    """
    <div style="text-align: center;">
        Made by <a href="https://github.com/satvik314/educhain" target="_blank">educhain</a> | Powered by Sutra LLM
    </div>
    """,
    unsafe_allow_html=True
)
