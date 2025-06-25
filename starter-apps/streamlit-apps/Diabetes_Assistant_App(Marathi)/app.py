import streamlit as st
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
import google.generativeai as genai
from mem0 import MemoryClient
import time

# Configure page
st.set_page_config(
    page_title="Diabetes Health Assistant",
    page_icon="🩺",
    layout="centered"
)

# Initialize APIs
@st.cache_resource
def initialize_apis():
    # Access API keys from st.secrets
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    MEM0_API_KEY = st.secrets["MEM0_API_KEY"]
    SUTRA_API_KEY = st.secrets["SUTRA_API_KEY"]

    # Configure Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    gemini = genai.GenerativeModel("gemini-1.5-flash")

    # Initialize Mem0 Client
    client = MemoryClient(api_key=MEM0_API_KEY)

    # Initialize SUTRA Agent
    sutra_agent = Agent(
        model=OpenAILike(
            id="sutra-v2",
            api_key=SUTRA_API_KEY,
            base_url="https://api.two.ai/v2"
        ),
        markdown=True,
        description="A multilingual medical assistant powered by SUTRA-V2",
        instructions=["Answer concisely in the requested language."]
    )

    return gemini, client, sutra_agent

# Initialize session state
def init_session_state():
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'is_new_user' not in st.session_state:
        st.session_state.is_new_user = None
    if 'registration_step' not in st.session_state:
        st.session_state.registration_step = 0
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'registration_complete' not in st.session_state:
        st.session_state.registration_complete = False
    if 'apis_initialized' not in st.session_state:
        st.session_state.apis_initialized = False

def process_input_with_translation(text, sutra_agent):
    """Process input with language detection and translation"""
    try:
        detect_prompt = f"Detect language of this: {text} (only 'en' or 'mr')"
        response = sutra_agent.run(detect_prompt)
        lang = response.content.strip().lower()

        if lang == 'mr':
            translate_prompt = f"Translate this Marathi to English: {text}"
            response = sutra_agent.run(translate_prompt)
            return response.content.strip(), 'mr'
        else:
            return text, 'en'
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text, 'en'

def check_existing_user(user_id, client):
    """Check if user exists in Mem0 database"""
    try:
        search_results = client.search("check", user_id=user_id)
        return len(search_results) > 0, search_results
    except Exception as e:
        st.error(f"Error checking user: {str(e)}")
        return False, []

def save_user_info(user_id, user_info, client):
    """Save user information to Mem0"""
    try:
        messages = [
            {"role": "user", "content": f"My name is {user_info['name']}."},
            {"role": "user", "content": f"I am {user_info['age']} years old."},
            {"role": "user", "content": f"I am a {user_info['gender']}."},
            {"role": "user", "content": f"I have {user_info['diabetes_type']} diabetes."},
            {"role": "user", "content": f"My medications include: {user_info['medication']}."},
            {"role": "user", "content": f"My symptoms include: {user_info['symptoms']}."},
            {"role": "user", "content": f"I currently live in: {user_info['location']}."},
            {"role": "assistant", "content": f"Thanks {user_info['name']}, your health info is stored for personalized support."}
        ]
        client.add(messages, user_id=user_id)
        return True
    except Exception as e:
        st.error(f"Error saving user info: {str(e)}")
        return False

def get_chat_response(query, user_id, detected_lang, gemini, client, sutra_agent):
    """Get response from AI models with context"""
    try:
        # Translate Marathi to English if needed
        if detected_lang == 'mr':
            translate_prompt = f"Translate to English: {query}"
            response = sutra_agent.run(translate_prompt)
            query_en = response.content
        else:
            query_en = query

        # Retrieve Mem0 context
        search_results = client.search(query_en, user_id=user_id)

        # Collect context from both 'message' and 'memory'
        mem0_memories = []
        for r in search_results:
            if 'message' in r and 'content' in r['message']:
                role = r['message'].get('role', 'user').capitalize()
                content = r['message']['content']
                mem0_memories.append(f"{role}: {content}")
            elif 'memory' in r:
                mem0_memories.append(f"Memory: {r['memory']}")

        context = "\n".join(mem0_memories)

        # Extract Personal Info
        user_name = "User"
        diabetes_type = "Not specified"
        location = "Not specified"

        for r in search_results:
            memory_text = ''
            if 'message' in r and 'content' in r['message']:
                memory_text = r['message']['content'].lower()
            elif 'memory' in r:
                memory_text = r['memory'].lower()

            if memory_text:
                if "name is" in memory_text:
                    user_name = memory_text.split("name is")[-1].split()[0].capitalize()
                if "type 1" in memory_text or "type 2" in memory_text:
                    diabetes_type = "Type 2" if "type 2" in memory_text else "Type 1"
                if "live in" in memory_text:
                    location = memory_text.split("live in")[-1].split(".")[0].strip().capitalize()

        # Create appropriate prompt based on detected language
        if detected_lang == 'mr':
            final_prompt = f"""
तुम्ही एक मधुमेह सहाय्यक आहात. {user_name} नावाच्या रुग्णाला {location} येथील {diabetes_type} मधुमेह असलेल्या रुग्णास मदत करत आहात.

पूर्वीच्या संभाषणातील आठवणी:
{context}

वापरकर्त्याचा नवीन प्रश्न:
"{query_en}"

भारतासाठी उपयुक्त, मधुमेह-सुरक्षित आणि व्यावहारिक उत्तर द्या.
"""
        else:
            final_prompt = f"""
You are a diabetes-friendly AI assistant helping {user_name}, a patient from {location} diagnosed with {diabetes_type} Diabetes.

Past memories from previous chats:
{context}

User's new query:
"{query_en}"

Provide a helpful, India-specific, diabetes-safe, and practical response.
"""

        # Generate response with Gemini
        response = gemini.generate_content(final_prompt)

        # Translate output to Marathi if needed
        if detected_lang == 'mr':
            translate_back_prompt = f"Translate this to Marathi: {response.text}"
            response_back = sutra_agent.run(translate_back_prompt)
            final_response = response_back.content
        else:
            final_response = response.text

        # Store the conversation in memory
        new_messages = [
            {"role": "user", "content": query},
            {"role": "assistant", "content": final_response}
        ]
        client.add(new_messages, user_id=user_id)

        return final_response

    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "Sorry, I encountered an error while processing your request. Please try again."

# Initialize session state and APIs
init_session_state()

# Initialize APIs
if not st.session_state.apis_initialized:
    with st.spinner("Initializing AI systems..."):
        try:
            gemini, client, sutra_agent = initialize_apis()
            st.session_state.gemini = gemini
            st.session_state.client = client
            st.session_state.sutra_agent = sutra_agent
            st.session_state.apis_initialized = True
        except Exception as e:
            st.error(f"Failed to initialize APIs: {str(e)}")
            st.stop()

# Main app header
st.title("🩺 Diabetes Health Assistant")
st.markdown("*Your personalized diabetes management companion*")
st.markdown("---")

# Step 1: User ID Input (always shown first)
if st.session_state.user_id is None:
    st.markdown("### Welcome! Please enter your details to continue")

    with st.form("user_login_form"):
        user_id = st.text_input(
            "Enter your unique username or ID:",
            placeholder="e.g., john_doe_123",
            help="This helps us personalize your experience"
        )
        submit_login = st.form_submit_button("Continue", use_container_width=True)

        if submit_login and user_id.strip():
            with st.spinner("Checking user database..."):
                st.session_state.user_id = user_id.strip()

                # Check if user exists
                user_exists, search_results = check_existing_user(
                    st.session_state.user_id,
                    st.session_state.client
                )

                if user_exists:
                    st.session_state.is_new_user = False
                    st.session_state.registration_complete = True
                    st.success("✅ Existing user detected. Welcome back!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.session_state.is_new_user = True
                    st.info("New user detected. Let's collect some basic information.")
                    time.sleep(1)
                    st.rerun()
        elif submit_login:
            st.error("Please enter a valid username or ID")

# Step 2: New User Registration (step by step)
elif st.session_state.is_new_user and not st.session_state.registration_complete:
    st.markdown(f"### Registration - Step {st.session_state.registration_step + 1} of 7")
    st.markdown(f"**User ID:** {st.session_state.user_id}")

    # Progress bar
    progress = (st.session_state.registration_step) / 7
    st.progress(progress)

    questions = [
        {
            "key": "name",
            "question_en": "What's your full name?",
            "question_mr": "तुमचं पूर्ण नाव काय आहे?",
            "placeholder": "Enter your full name",
            "input_type": "text"
        },
        {
            "key": "age",
            "question_en": "What is your age?",
            "question_mr": "तुमचं वय किती आहे?",
            "placeholder": "Enter your age",
            "input_type": "number"
        },
        {
            "key": "gender",
            "question_en": "What is your gender?",
            "question_mr": "तुमचे लिंग काय आहे?",
            "placeholder": "e.g., Male, Female, Other",
            "input_type": "text"
        },
        {
            "key": "diabetes_type",
            "question_en": "What type of Diabetes do you have?",
            "question_mr": "डायबिटीजचा प्रकार?",
            "placeholder": "e.g., Type 1, Type 2, Gestational",
            "input_type": "text"
        },
        {
            "key": "medication",
            "question_en": "What medications are you currently taking?",
            "question_mr": "कोणती औषधे घेतलीत?",
            "placeholder": "List your current medications",
            "input_type": "text_area"
        },
        {
            "key": "symptoms",
            "question_en": "Are you experiencing any unusual symptoms?",
            "question_mr": "काही लक्षणे?",
            "placeholder": "Describe any symptoms you're experiencing",
            "input_type": "text_area"
        },
        {
            "key": "location",
            "question_en": "Where are you currently living?",
            "question_mr": "तुम्ही सध्या कुठे राहता?",
            "placeholder": "City, State",
            "input_type": "text"
        }
    ]

    if st.session_state.registration_step < len(questions):
        current_q = questions[st.session_state.registration_step]

        with st.form(f"registration_step_{st.session_state.registration_step}"):
            st.markdown(f"**{current_q['question_en']}**")
            st.markdown(f"*{current_q['question_mr']}*")

            # Different input types based on question
            if current_q['input_type'] == 'number':
                answer = st.number_input(
                    "Your answer:",
                    min_value=1,
                    max_value=120,
                    value=None,
                    placeholder=current_q['placeholder'],
                    label_visibility="collapsed"
                )
                answer = str(answer) if answer is not None else ""
            elif current_q['input_type'] == 'text_area':
                answer = st.text_area(
                    "Your answer:",
                    placeholder=current_q['placeholder'],
                    label_visibility="collapsed",
                    height=100
                )
            else:
                answer = st.text_input(
                    "Your answer:",
                    placeholder=current_q['placeholder'],
                    label_visibility="collapsed"
                )

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.form_submit_button("⬅️ Previous") and st.session_state.registration_step > 0:
                    st.session_state.registration_step -= 1
                    st.rerun()

            with col2:
                if st.form_submit_button("Next ➡️", use_container_width=True):
                    if str(answer).strip():
                        # Process language detection and translation
                        with st.spinner("Processing..."):
                            processed_answer, detected_lang = process_input_with_translation(
                                str(answer),
                                st.session_state.sutra_agent
                            )
                            st.session_state.user_info[current_q['key']] = processed_answer
                            st.session_state.registration_step += 1
                            st.rerun()
                    else:
                        st.error("Please provide an answer before continuing")

    # Registration complete
    if st.session_state.registration_step >= len(questions):
        st.success("🎉 Registration Complete!")
        st.markdown("### Your Information Summary:")

        info_display = {
            "name": "Full Name",
            "age": "Age",
            "gender": "Gender",
            "diabetes_type": "Diabetes Type",
            "medication": "Current Medications",
            "symptoms": "Symptoms",
            "location": "Location"
        }

        for key, label in info_display.items():
            if key in st.session_state.user_info:
                st.markdown(f"**{label}:** {st.session_state.user_info[key]}")

        if st.button("Start Chatting! 💬", use_container_width=True):
            with st.spinner("Saving your information..."):
                # Save user info to database
                success = save_user_info(
                    st.session_state.user_id,
                    st.session_state.user_info,
                    st.session_state.client
                )

                if success:
                    st.session_state.registration_complete = True
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"Thanks {st.session_state.user_info.get('name', 'there')}, your health info is stored for personalized support. How can I help you today?"
                    })
                    st.rerun()
                else:
                    st.error("Failed to save your information. Please try again.")

# Step 3: Chat Interface (for registered users)
elif st.session_state.registration_complete:
    # Welcome message for existing users
    if st.session_state.is_new_user == False and len(st.session_state.chat_history) == 0:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Welcome back! How can I assist you with your diabetes management today?"
        })

    # Display user info in sidebar
    with st.sidebar:
        st.markdown("### Your Profile")
        st.markdown(f"**User ID:** {st.session_state.user_id}")
        if st.session_state.user_info:
            st.markdown(f"**Name:** {st.session_state.user_info.get('name', 'N/A')}")
            st.markdown(f"**Age:** {st.session_state.user_info.get('age', 'N/A')}")
            st.markdown(f"**Gender:** {st.session_state.user_info.get('gender', 'N/A')}")
            st.markdown(f"**Diabetes Type:** {st.session_state.user_info.get('diabetes_type', 'N/A')}")
            st.markdown(f"**Location:** {st.session_state.user_info.get('location', 'N/A')}")

        st.markdown("---")

        if st.button("🔄 Reset Chat"):
            st.session_state.chat_history = []
            st.rerun()

        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Chat history display
    st.markdown("### Chat History")

    # Container for chat messages
    chat_container = st.container()

    with chat_container:
        if len(st.session_state.chat_history) == 0:
            st.info("Start a conversation by typing your question below!")
        else:
            for i, message in enumerate(st.session_state.chat_history):
                if message["role"] == "user":
                    with st.chat_message("user"):
                        st.write(message["content"])
                else:
                    with st.chat_message("assistant"):
                        st.write(message["content"])

    # Chat input (always at bottom)
    st.markdown("---")

    # Input form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Your message:",
            placeholder="Ask me anything about diabetes management... (English/मराठी)",
            label_visibility="collapsed",
            height=100
        )

        col1, col2 = st.columns([4, 1])
        with col2:
            submit_chat = st.form_submit_button("Send 📤", use_container_width=True)

        if submit_chat and user_input.strip():
            # Add user message to chat history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input.strip()
            })

            # Process the input and get response
            with st.spinner("Thinking..."):
                # Detect language
                processed_input, detected_lang = process_input_with_translation(
                    user_input.strip(),
                    st.session_state.sutra_agent
                )

                # Get AI response
                response = get_chat_response(
                    user_input.strip(),
                    st.session_state.user_id,
                    detected_lang,
                    st.session_state.gemini,
                    st.session_state.client,
                    st.session_state.sutra_agent
                )

            # Add assistant response to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })

            # Rerun to update the display
            st.rerun()

        elif submit_chat:
            st.error("Please enter a message before sending")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <small>Diabetes Health Assistant - Stay healthy! 🌟</small>
    </div>
    """,
    unsafe_allow_html=True
)
