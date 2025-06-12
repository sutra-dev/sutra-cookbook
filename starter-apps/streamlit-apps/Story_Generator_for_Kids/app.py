import streamlit as st
import os
from typing import Optional, List, Type, Any
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Page configuration with kid-friendly icon
st.set_page_config(
    page_title="Story Generator for Kids",
    page_icon="📚",
    layout="wide"
)

# Define languages with their native names for better representation
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
    "Odia (ଓଡ଼ିଆ)", 
    "Sanskrit (संस्कृतम्)",
    "Nepali (नेपाली)",
    "Konkani (कोंकणी)",
    "Manipuri (মৈতৈলোন्)",
    "Kashmiri (कॉशुर)",
    "Santali (ᱥᱟᱱᱛᱟᱲᱤ)",
    "Sindhi (سنڌي)",
    "Bodo (बड़ो)",
    "Dogri (डोगरी)"
]

# Story themes for kids
story_themes = [
    "Adventure", 
    "Friendship", 
    "Animals", 
    "Magic", 
    "Family",
    "Outer Space", 
    "Underwater World", 
    "Fairy Tales", 
    "Superheroes", 
    "Nature",
    "School", 
    "Holidays", 
    "Seasons", 
    "Sports", 
    "Music",
    "Vehicles", 
    "Mystery", 
    "History", 
    "Science", 
    "Art",
    "Food", 
    "Travel", 
    "Dreams", 
    "Festivals"
]

# Age groups
age_groups = [
    "3-5 years (Preschool)",
    "6-8 years (Early Elementary)",
    "9-12 years (Upper Elementary)"
]

# Story length options
story_lengths = {
    "Short (2-3 minutes)": "short",
    "Medium (5-7 minutes)": "medium",
    "Long (10-15 minutes)": "long"
}

# Character types
character_types = [
    "Children", 
    "Animals", 
    "Magical Creatures", 
    "Toys", 
    "Plants",
    "Robots", 
    "Aliens", 
    "Historical Figures", 
    "Cartoon Characters", 
    "Everyday Objects"
]

# Settings for stories
story_settings = [
    "Forest", 
    "Beach", 
    "Mountains", 
    "City", 
    "Village",
    "School", 
    "Space", 
    "Underwater", 
    "Desert", 
    "Jungle",
    "Castle", 
    "Farm", 
    "Island", 
    "Playground", 
    "Home",
    "Imaginary World", 
    "Ancient Kingdom", 
    "Future City", 
    "Arctic", 
    "Rainforest"
]

# Story moral values
moral_values = [
    "Honesty", 
    "Kindness", 
    "Courage", 
    "Perseverance", 
    "Friendship",
    "Sharing", 
    "Respect", 
    "Responsibility", 
    "Patience", 
    "Cooperation",
    "Gratitude", 
    "Empathy", 
    "Forgiveness", 
    "Generosity", 
    "Self-confidence",
    "Hard work", 
    "Creativity", 
    "Curiosity", 
    "Helpfulness", 
    "Humility"
]

# Define character names by culture
character_names = {
    "Indian": ["Aarav", "Advait", "Arjun", "Dhruv", "Ishaan", "Kabir", "Reyansh", "Vihaan", "Vivaan", "Zayan", 
               "Aanya", "Diya", "Kiara", "Myra", "Pari", "Saanvi", "Samaira", "Shanaya", "Tara", "Zara"],
    "International": ["Alex", "Ben", "Charlie", "Daniel", "Ethan", "Felix", "George", "Henry", "Isaac", "Jack",
                      "Amelia", "Bella", "Chloe", "Daisy", "Emma", "Freya", "Grace", "Hannah", "Ivy", "Julia"],
    "Fantasy": ["Auryn", "Blade", "Cosmos", "Drax", "Eldin", "Flare", "Glimmer", "Helix", "Ignis", "Jinx",
                "Astra", "Brynn", "Crystal", "Delphi", "Echo", "Fable", "Gaia", "Halo", "Iris", "Jewel"]
}

# Story structure
class StoryCharacter(BaseModel):
    name: str = Field(..., description="The name of the character")
    description: str = Field(..., description="Brief description of the character")

class Story(BaseModel):
    title: str = Field(..., description="An engaging and age-appropriate title for the story")
    characters: List[StoryCharacter] = Field(..., description="List of main characters in the story")
    content: str = Field(..., description="The complete story text")
    moral: Optional[str] = Field(None, description="The moral or lesson of the story, if applicable")
    fun_question: Optional[str] = Field(None, description="An engaging question to ask the child after the story")

class LLMConfig:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "sutra-v2",
        max_tokens: int = 2500,
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

class StoryGenerator:
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
    
    def generate_story(
        self,
        theme: str,
        language: str,
        age_group: str,
        story_length: str,
        character_type: str,
        setting: str,
        moral: str,
        name_style: str,
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        llm: Optional[Any] = None,
    ) -> Story:
        if response_model is None:
            response_model = Story
        parser = PydanticOutputParser(pydantic_object=response_model)
        format_instructions = parser.get_format_instructions()

        # Character names based on selected style
        possible_names = character_names.get(name_style, character_names["Fantasy"])
        random_names = random.sample(possible_names, min(3, len(possible_names)))
        character_name_examples = ", ".join(random_names)

        if prompt_template is None:
            prompt_template = """
            You are an expert children's story writer specializing in creating engaging, educational, and 
            culturally appropriate stories for young readers. Your task is to create a delightful story 
            based on the following parameters:

            IMPORTANT LANGUAGE INSTRUCTION: Write the ENTIRE story in {language} language with proper grammar, 
            natural phrasing, and culturally appropriate context as if written by a native speaker. 
            Use simple vocabulary and sentence structure appropriate for the specified age group.

            STORY PARAMETERS:
            - Theme: {theme}
            - Target Age: {age_group}
            - Length: {story_length} 
            - Main Character Type: {character_type}
            - Setting: {setting}
            - Moral/Value to Convey: {moral}
            - Character Name Style: Names like {character_name_examples}

            STORY WRITING GUIDELINES:
            1. CREATE AGE-APPROPRIATE CONTENT:
               - For 3-5 years: Use very simple language, repetition, and rhymes. Keep sentences short.
               - For 6-8 years: Use clear language with some new vocabulary. Include simple dialogue.
               - For 9-12 years: Use more complex sentence structures and vocabulary with nuanced themes.

            2. LENGTH GUIDELINES:
               - Short: 300-400 words (~2-3 minutes read-aloud time)
               - Medium: 500-700 words (~5-7 minutes read-aloud time)
               - Long: 800-1200 words (~10-15 minutes read-aloud time)

            3. STORY STRUCTURE:
               - Begin with an engaging opening that introduces the main character(s)
               - Present a problem or challenge appropriate to the age group
               - Develop the story with age-appropriate tension/excitement
               - Resolve the conflict in a satisfying way
               - End with a clear conclusion that reinforces the moral/value

            4. CULTURAL SENSITIVITY:
               - Incorporate culturally relevant elements if writing in a regional language
               - Avoid stereotypes and ensure respectful representation
               - Use culturally appropriate names, settings, and references

            5. EDUCATIONAL VALUE:
               - Naturally embed the specified moral/value without being preachy
               - Include 2-3 new vocabulary words appropriate for the age group
               - Make the story both entertaining and enriching

            6. ENGAGEMENT ELEMENTS:
               - Include sensory details (sights, sounds, smells, textures)
               - Add elements of surprise, humor, or wonder
               - Create memorable characters that children can relate to
               - For younger ages, include opportunities for interaction (questions, sound effects)

            IMPORTANT NOTES:
            - Ensure complete safety and appropriateness for children
            - Avoid any frightening elements, violence, or mature themes
            - Make the story engaging, positive, and uplifting
            - End with a gentle moral that reinforces positive values

            The output must include:
            - An age-appropriate title
            - A list of main characters with brief descriptions
            - The complete story text
            - A moral or lesson from the story
            - A fun question to engage the child after the story
            """

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        prompt_template += "\n\nThe response should be in JSON format.\n{format_instructions}"

        story_prompt = PromptTemplate(
            input_variables=["theme", "language", "age_group", "story_length", "character_type", 
                            "setting", "moral", "character_name_examples"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        llm_to_use = llm if llm is not None else self.llm
        story_chain = story_prompt | llm_to_use
        results = story_chain.invoke({
            "theme": theme, 
            "language": language, 
            "age_group": age_group, 
            "story_length": story_length, 
            "character_type": character_type, 
            "setting": setting, 
            "moral": moral,
            "character_name_examples": character_name_examples
        })

        try:
            structured_output = parser.parse(results.content)
            return structured_output
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:")
            print(results.content)
            # Return a default story in case of parsing error
            return Story(
                title="Story Generation Issue",
                characters=[StoryCharacter(name="Error", description="There was an issue generating the story")],
                content=results.content if hasattr(results, 'content') else str(results),
                moral="Sometimes technology needs a little help!",
                fun_question="Can you help create your own story instead?"
            )

# --- Sidebar Configuration ---
with st.sidebar:
    st.sidebar.image("https://framerusercontent.com/images/3Ca34Pogzn9I3a7uTsNSlfs9Bdk.png", use_container_width=True)
    st.header("Story Settings")
    
    # Use environment variable if available, otherwise hide API key input
    api_key = os.getenv("SUTRA_API_KEY", "")
    if not api_key:
        api_key = st.text_input("Sutra API Key", value="", type="password")
        if not api_key:
            st.warning("Please set your Sutra API Key as an environment variable or enter it above")
    
    # Language selection
    selected_language = st.selectbox("Story Language:", languages)
    selected_language = selected_language.split(" ")[0]  # Extract just the language name without native script
    
    # Age group
    age_group = st.selectbox("Age Group:", age_groups)
    
    # Story length
    story_length_display = st.selectbox("Story Length:", list(story_lengths.keys()))
    story_length = story_lengths[story_length_display]
    
    # Advanced options in expander
    with st.expander("Advanced Story Options"):
        character_type = st.selectbox("Main Character Type:", character_types)
        setting = st.selectbox("Story Setting:", story_settings)
        moral = st.selectbox("Moral/Value:", moral_values)
        name_style = st.selectbox("Character Name Style:", list(character_names.keys()))
    
    st.divider()
    st.caption("Powered by Sutra LLM")
    st.caption("Made with Streamlit")

# Initialize StoryGenerator with Sutra LLM if API key is provided
if api_key:
    llm_config = LLMConfig(api_key=api_key)
    story_generator = StoryGenerator(llm_config)

# --- Main UI ---
# Main header
st.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <h1>📚 Story Generator for Kids</h1>
    <p style="font-size: 1.2rem;">Create magical stories in regional languages!</p>
</div>
""", unsafe_allow_html=True)

# Language indicator
st.markdown(f"""
<div style="padding: 0.75rem; border-radius: 6px; margin-bottom: 1.5rem; border: 1px solid;">
    <span style="font-size: 1.25rem; margin-right: 8px;">🔤</span>
    <span>Currently creating stories in <strong>{selected_language}</strong></span>
</div>
""", unsafe_allow_html=True)

# Check if API key is available
if not api_key:
    st.warning("Please enter your Sutra API Key in the sidebar or set it as an environment variable to continue.")
    st.stop()

# Story theme selection with images
st.subheader("What kind of story would you like today?")
theme_cols = st.columns(4)
theme_options = {}

# Theme icons mapping
theme_icons = {
    "Adventure": "🧗‍♂️", "Friendship": "🤝", "Animals": "🐘", "Magic": "✨",
    "Family": "👨‍👩‍👧‍👦", "Outer Space": "🚀", "Underwater World": "🐙", "Fairy Tales": "🧚",
    "Superheroes": "🦸‍♀️", "Nature": "🌳", "School": "🏫", "Holidays": "🎁",
    "Seasons": "🍂", "Sports": "⚽", "Music": "🎵", "Vehicles": "🚗",
    "Mystery": "🔎", "History": "📜", "Science": "🔬", "Art": "🎨",
    "Food": "🍕", "Travel": "✈️", "Dreams": "💭", "Festivals": "🎭"
}

for i, theme in enumerate(story_themes):
    col_idx = i % 4
    with theme_cols[col_idx]:
        theme_key = f"theme_{i}"
        icon = theme_icons.get(theme, "📘")
        theme_options[theme] = st.button(f"{icon} {theme}", key=theme_key, use_container_width=True)

selected_theme = None
for theme, selected in theme_options.items():
    if selected:
        selected_theme = theme
        break

# Custom theme option
custom_theme_expander = st.expander("Or enter your own theme")
with custom_theme_expander:
    custom_theme = st.text_input("Enter a custom theme:", "")
    if st.button("Use Custom Theme", use_container_width=True):
        selected_theme = custom_theme

# Generate Story Button
if selected_theme:
    st.divider()
    st.subheader(f"Generating a {selected_theme} story")
    
    story_placeholder = st.empty()
    with story_placeholder.container():
        with st.spinner(f"✨ Creating your {selected_theme} story in {selected_language}... Please wait!"):
            story = story_generator.generate_story(
                theme=selected_theme,
                language=selected_language,
                age_group=age_group,
                story_length=story_length,
                character_type=character_type,
                setting=setting,
                moral=moral,
                name_style=name_style
            )
    
    # Display the story with nice formatting
    st.markdown(f"# {story.title}")
    
    # Display characters
    st.markdown("## Characters")
    for character in story.characters:
        st.markdown(f"**{character.name}**: {character.description}")
    
    st.divider()
    
    # Display story content
    st.markdown("## Story")
    st.markdown(story.content)
    
    st.divider()
    
    # Display moral and fun question
    if story.moral:
        st.markdown(f"**Moral of the story:** {story.moral}")
    
    if story.fun_question:
        st.markdown(f"**Let's talk about it:** {story.fun_question}")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 Create Another Story", use_container_width=True):
            st.rerun()
    with col2:
        st.download_button(
            label="📥 Save This Story",
            data=f"# {story.title}\n\n## Characters\n" + 
                 "\n".join([f"- **{c.name}**: {c.description}" for c in story.characters]) + 
                 f"\n\n## Story\n{story.content}\n\n" +
                 (f"**Moral:** {story.moral}\n" if story.moral else "") +
                 (f"**Fun Question:** {story.fun_question}" if story.fun_question else ""),
            file_name=f"{story.title}.md",
            mime="text/markdown",
            use_container_width=True
        )

else:
    # Display welcome message when no theme is selected
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ## Welcome to the Magic Story Factory!
        
        Choose a story theme from above to get started on your adventure!
        
        Our AI storyteller will create a unique story just for you in your chosen language,
        perfectly suited for the selected age group.
        
        Each story comes with:
        - Colorful characters
        - An exciting plot
        - A valuable moral lesson
        - A fun question to think about
        
        Ready to begin? Just click on a theme you like!
        """)
    
    with col2:
        st.image("https://img.icons8.com/dusk/128/storytelling.png", width=150)

# Footer
st.markdown("---")
st.caption("This application uses AI to generate children's stories in multiple languages. The stories are meant to be engaging, educational, and culturally appropriate.")
