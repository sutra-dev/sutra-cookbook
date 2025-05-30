import streamlit as st
from educhain import Educhain, LLMConfig
from educhain.engines import qna_engine
from langchain_openai import ChatOpenAI
import os
import json
from datetime import datetime
import pandas as pd
import random


# Set page configuration at the very top of the script
st.set_page_config(page_title="Multilingual Quiz App", page_icon="🧠", layout="wide")

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
question_types = ["Multiple Choice", "True/False"]

# Define difficulty levels
difficulty_levels = ["Easy", "Medium", "Hard"]

# Initialize session state
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = None
if 'quiz_in_progress' not in st.session_state:
    st.session_state.quiz_in_progress = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = []
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False
if 'saved_quizzes' not in st.session_state:
    st.session_state.saved_quizzes = []
if 'page' not in st.session_state:
    st.session_state.page = "create"  # Options: "create", "take", "history"

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("Create Multilingual Quiz")
    
    # Navigation
    st.subheader("📚 Navigation")
    if st.button("Create Quiz", use_container_width=True):
        st.session_state.page = "create"
    if st.button("Saved Quizzes", use_container_width=True):
        st.session_state.page = "saved"
    if st.button("Quiz History", use_container_width=True):
        st.session_state.page = "history"
    
    st.header("⚙️ Configuration")
    
    # API Key section
    st.markdown("### API Key")
    st.markdown("Get your free API key from [Sutra API](https://www.two.ai/sutra/api)")
    api_key = st.text_input("Enter your Sutra API Key:", type="password")
    
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

# --- Utility Function to Convert Questions to Quiz Format ---
def convert_to_quiz_format(questions_obj, topic, language, difficulty):
    quiz = {
        "title": f"{topic} Quiz ({difficulty})",
        "language": language,
        "difficulty": difficulty,
        "topic": topic,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "questions": []
    }
    
    if hasattr(questions_obj, "questions"):
        for q in questions_obj.questions:
            question_data = {
                "question": q.question,
                "answer": q.answer
            }
            
            if hasattr(q, 'options'):
                question_data["type"] = "multiple_choice"
                question_data["options"] = q.options
            else:
                question_data["type"] = "true_false"
                question_data["options"] = ["True", "False"]
                
            if hasattr(q, 'explanation') and q.explanation:
                question_data["explanation"] = q.explanation
                
            quiz["questions"].append(question_data)
    
    return quiz

# --- Save Quiz Function ---
def save_quiz(quiz):
    # Create a unique ID for the quiz
    quiz_id = f"{len(st.session_state.saved_quizzes) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    quiz["id"] = quiz_id
    
    # Add to saved quizzes
    st.session_state.saved_quizzes.append(quiz)
    
    # Also save to disk (optional)
    try:
        # Check if file exists and load existing data
        if os.path.exists("saved_quizzes.json"):
            with open("saved_quizzes.json", "r") as f:
                existing_quizzes = json.load(f)
        else:
            existing_quizzes = []
            
        # Append new quiz
        existing_quizzes.append(quiz)
        
        # Save updated list
        with open("saved_quizzes.json", "w") as f:
            json.dump(existing_quizzes, f)
    except Exception as e:
        st.warning(f"Could not save quiz to disk: {str(e)}")
    
    return quiz_id

# --- Start Quiz Function ---
def start_quiz(quiz):
    st.session_state.current_quiz = quiz
    st.session_state.quiz_in_progress = True
    st.session_state.current_question = 0
    st.session_state.user_answers = [None] * len(quiz["questions"])
    st.session_state.user_score = 0
    st.session_state.quiz_completed = False

# --- Submit Answer Function ---
def submit_answer(answer_index):
    current_q = st.session_state.current_question
    st.session_state.user_answers[current_q] = answer_index
    
    # Check if answer is correct
    correct_answer = st.session_state.current_quiz["questions"][current_q]["answer"]
    
    # For multiple choice, the answer might be the option text or the option index
    if st.session_state.current_quiz["questions"][current_q]["type"] == "multiple_choice":
        # Try to match by index first (if answer is A, B, C, D)
        if correct_answer in ["A", "B", "C", "D"]:
            correct_index = ord(correct_answer) - ord("A")
            if answer_index == correct_index:
                st.session_state.user_score += 1
        # Otherwise, match by option text
        else:
            options = st.session_state.current_quiz["questions"][current_q]["options"]
            if answer_index < len(options) and options[answer_index] == correct_answer:
                st.session_state.user_score += 1
    # For true/false
    else:
        options = ["True", "False"]
        user_answer = options[answer_index]
        # Convert both answers to lowercase strings for comparison
        if str(user_answer).lower() == str(correct_answer).lower():
            st.session_state.user_score += 1
    
    # Move to next question or end quiz
    if current_q < len(st.session_state.current_quiz["questions"]) - 1:
        st.session_state.current_question += 1
    else:
        st.session_state.quiz_completed = True
        # Save quiz results to history
        save_quiz_result()

# --- Save Quiz Result Function ---
def save_quiz_result():
    result = {
        "quiz_title": st.session_state.current_quiz["title"],
        "language": st.session_state.current_quiz["language"],
        "topic": st.session_state.current_quiz["topic"],
        "difficulty": st.session_state.current_quiz["difficulty"],
        "score": st.session_state.user_score,
        "total": len(st.session_state.current_quiz["questions"]),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    # Initialize history if not exists
    if 'quiz_history' not in st.session_state:
        st.session_state.quiz_history = []
    
    # Add to history
    st.session_state.quiz_history.append(result)
    
    # Also save to disk (optional)
    try:
        # Check if file exists and load existing data
        if os.path.exists("quiz_history.json"):
            with open("quiz_history.json", "r") as f:
                existing_history = json.load(f)
        else:
            existing_history = []
            
        # Append new result
        existing_history.append(result)
        
        # Save updated list
        with open("quiz_history.json", "w") as f:
            json.dump(existing_history, f)
    except Exception as e:
        st.warning(f"Could not save quiz history to disk: {str(e)}")

# --- Create Quiz Page ---
def show_create_quiz_page():
    st.markdown(
        f'<h1><img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png" width="60"/> Multilingual Quiz App</h1>',
        unsafe_allow_html=True
    )
    
    # --- Initialize Educhain client if API key is provided ---
    if not api_key:
        st.warning("Please enter your Sutra API Key in the sidebar to continue.")
        return

    educhain_client = initialize_educhain(api_key)
    if not educhain_client:
        st.error("Failed to initialize Educhain. Please check your Sutra API key.")
        return

    qna_engine = educhain_client.qna_engine
    
    # Quiz configuration
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_language = st.selectbox("Language:", languages)
    with col2:
        selected_question_type = st.selectbox("Question Type:", question_types)
    with col3:
        selected_difficulty = st.selectbox("Difficulty:", difficulty_levels)
    
    topic = st.text_input("Quiz Topic:", "General Knowledge")
    num_questions = st.slider("Number of Questions", 3, 10, 5)
    
    custom_instructions = st.text_area(
        "Custom Instructions (optional):", 
        placeholder=f"e.g. 'Focus on {selected_difficulty.lower()} concepts for {topic}'",
        height=100
    )
    
    # Add language instruction to custom instructions
    language_custom_instructions = f"Generate all questions, options, answers and explanations in {selected_language} language. Make questions {selected_difficulty.lower()} difficulty. {custom_instructions}"
    
    # Generate quiz button
    if st.button("Generate Quiz"):
        with st.spinner(f"Generating {num_questions} {selected_question_type.lower()} questions in {selected_language}..."):
            try:
                # Use the appropriate method based on question type
                if selected_question_type == "Multiple Choice":
                    questions = qna_engine.generate_questions(
                        topic=topic,
                        num=num_questions,
                        question_type="Multiple Choice",
                        custom_instructions=language_custom_instructions,
                        difficulty=selected_difficulty.lower(),
                        language=selected_language
                    )
                else:  # True/False
                    questions = qna_engine.generate_questions(
                        topic=topic,
                        num=num_questions,
                        question_type="True/False",
                        custom_instructions=language_custom_instructions,
                        difficulty=selected_difficulty.lower(),
                        language=selected_language
                    )
                
                if not questions or not hasattr(questions, "questions"):
                    st.error("Failed to generate questions. Please try again with different parameters.")
                    return
                
                # Convert to quiz format and save
                quiz = convert_to_quiz_format(questions, topic, selected_language, selected_difficulty)
                quiz_id = save_quiz(quiz)
                
                st.success(f"Quiz generated successfully! Quiz ID: {quiz_id}")
                
                # Preview quiz
                with st.expander("Preview Quiz"):
                    for i, q in enumerate(quiz["questions"]):
                        st.subheader(f"Question {i+1}: {q['question']}")
                        st.write("Options:")
                        for j, opt in enumerate(q["options"]):
                            st.write(f"   {chr(65 + j)}. {opt}")
                        st.write(f"**Correct Answer:** {q['answer']}")
                        if "explanation" in q and q["explanation"]:
                            st.write(f"**Explanation:** {q['explanation']}")
                        st.markdown("---")
                
                # Button to start quiz
                if st.button("Start This Quiz"):
                    start_quiz(quiz)
                    st.session_state.page = "take"
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Error generating questions: {str(e)}")
                st.error("Please try again with different parameters or check your API key.")

# --- Saved Quizzes Page ---
def show_saved_quizzes_page():
    st.markdown(
        f'<h1><img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png" width="60"/> Saved Quizzes</h1>',
        unsafe_allow_html=True
    )
    
    if not st.session_state.saved_quizzes:
        st.info("No saved quizzes yet. Create one first!")
        return
    
    # Create a dataframe for better display
    quiz_data = []
    for quiz in st.session_state.saved_quizzes:
        quiz_data.append({
            "ID": quiz.get("id", "Unknown"),
            "Title": quiz.get("title", "Untitled"),
            "Topic": quiz.get("topic", "Unknown"),
            "Language": quiz.get("language", "Unknown"),
            "Difficulty": quiz.get("difficulty", "Unknown"),
            "Questions": len(quiz.get("questions", [])),
            "Created": quiz.get("created_at", "Unknown")
        })
    
    df = pd.DataFrame(quiz_data)
    st.dataframe(df, use_container_width=True)
    
    # Select quiz to take
    selected_quiz_id = st.selectbox(
        "Select a quiz to take:", 
        options=[quiz.get("id", "Unknown") for quiz in st.session_state.saved_quizzes],
        format_func=lambda x: next((q["title"] for q in st.session_state.saved_quizzes if q.get("id") == x), x)
    )
    
    # Start selected quiz
    if st.button("Start Selected Quiz"):
        selected_quiz = next((q for q in st.session_state.saved_quizzes if q.get("id") == selected_quiz_id), None)
        if selected_quiz:
            start_quiz(selected_quiz)
            st.session_state.page = "take"
            st.rerun()
    
    # Option to delete a quiz
    if st.button("Delete Selected Quiz"):
        st.session_state.saved_quizzes = [q for q in st.session_state.saved_quizzes if q.get("id") != selected_quiz_id]
        st.success("Quiz deleted successfully!")
        st.rerun()

# --- Take Quiz Page ---
def show_take_quiz_page():
    if not st.session_state.quiz_in_progress or not st.session_state.current_quiz:
        st.warning("No quiz is currently in progress.")
        if st.button("Go to Saved Quizzes"):
            st.session_state.page = "saved"
            st.rerun()
        return
    
    quiz = st.session_state.current_quiz
    
    # Display quiz header
    st.markdown(
        f'<h1>{quiz["title"]}</h1>', 
        unsafe_allow_html=True
    )
    st.write(f"Language: {quiz['language']} | Difficulty: {quiz['difficulty']} | Topic: {quiz['topic']}")
    
    # If quiz is completed, show results
    if st.session_state.quiz_completed:
        st.balloons()
        st.markdown(f"## Quiz Completed!")
        st.markdown(f"### Your Score: {st.session_state.user_score}/{len(quiz['questions'])}")
        
        # Calculate percentage
        percentage = (st.session_state.user_score / len(quiz['questions'])) * 100
        st.progress(percentage / 100)
        
        # Different messages based on score
        if percentage >= 80:
            st.success("Excellent! You've mastered this topic!")
        elif percentage >= 60:
            st.info("Good job! You have a solid understanding of the material.")
        else:
            st.warning("You might want to review this topic again.")
        
        # Show answers and explanations
        with st.expander("Review Questions and Answers"):
            for i, (question, user_answer) in enumerate(zip(quiz["questions"], st.session_state.user_answers)):
                correct_answer = question["answer"]
                is_correct = False
                
                # Determine if the answer was correct
                if question["type"] == "multiple_choice":
                    if correct_answer in ["A", "B", "C", "D"]:
                        correct_index = ord(correct_answer) - ord("A")
                        is_correct = (user_answer == correct_index)
                    else:
                        is_correct = (question["options"][user_answer] == correct_answer)
                else:  # true/false
                    options = ["True", "False"]
                    # Convert both answers to lowercase strings for comparison
                    is_correct = (str(options[user_answer]).lower() == str(correct_answer).lower())
                
                # Display question and answer
                st.markdown(f"**Question {i+1}:** {question['question']}")
                
                if question["type"] == "multiple_choice":
                    st.write("Options:")
                    for j, opt in enumerate(question["options"]):
                        prefix = "✅ " if (is_correct and user_answer == j) else "❌ " if (not is_correct and user_answer == j) else ""
                        highlight = "**" if (correct_answer in ["A", "B", "C", "D"] and j == ord(correct_answer) - ord("A")) or \
                                          (correct_answer not in ["A", "B", "C", "D"] and opt == correct_answer) else ""
                        st.write(f"   {prefix}{chr(65 + j)}. {highlight}{opt}{highlight}")
                else:  # true/false
                    st.write("Options:")
                    for j, opt in enumerate(["True", "False"]):
                        prefix = "✅ " if (is_correct and user_answer == j) else "❌ " if (not is_correct and user_answer == j) else ""
                        highlight = "**" if str(opt).lower() == str(correct_answer).lower() else ""
                        st.write(f"   {prefix}{opt} {highlight}")
                
                if "explanation" in question and question["explanation"]:
                    st.write(f"**Explanation:** {question['explanation']}")
                
                st.markdown("---")
        
        # Button to go back to saved quizzes
        if st.button("Choose Another Quiz"):
            st.session_state.page = "saved"
            st.rerun()
            
        # Button to create a new quiz
        if st.button("Create New Quiz"):
            st.session_state.page = "create"
            st.rerun()
    
    # If quiz is in progress, show current question
    else:
        current_q_index = st.session_state.current_question
        total_questions = len(quiz["questions"])
        current_q = quiz["questions"][current_q_index]
        
        # Progress bar
        st.progress((current_q_index) / total_questions)
        st.write(f"Question {current_q_index + 1} of {total_questions}")
        
        # Display question
        st.markdown(f"## {current_q['question']}")
        
        # Display options based on question type
        if current_q["type"] == "multiple_choice":
            for i, option in enumerate(current_q["options"]):
                if st.button(f"{chr(65 + i)}. {option}", key=f"opt_{i}"):
                    submit_answer(i)
                    st.rerun()
        else:  # true/false
            col1, col2 = st.columns(2)
            with col1:
                if st.button("True", use_container_width=True):
                    submit_answer(0)
                    st.rerun()
            with col2:
                if st.button("False", use_container_width=True):
                    submit_answer(1)
                    st.rerun()
        
        # Option to skip question
        if st.button("Skip Question"):
            submit_answer(random.randint(0, len(current_q["options"]) - 1))  # Submit random answer
            st.rerun()

# --- Quiz History Page ---
def show_history_page():
    st.markdown(
        f'<h1><img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png" width="60"/> Quiz History</h1>',
        unsafe_allow_html=True
    )
    
    # Initialize quiz_history if not exists
    if 'quiz_history' not in st.session_state:
        st.session_state.quiz_history = []
        
        # Try to load from disk
        try:
            if os.path.exists("quiz_history.json"):
                with open("quiz_history.json", "r") as f:
                    st.session_state.quiz_history = json.load(f)
        except Exception:
            pass
    
    if not st.session_state.quiz_history:
        st.info("No quiz history yet. Take a quiz first!")
        return
    
    # Create a dataframe for better display
    history_data = []
    for result in st.session_state.quiz_history:
        percentage = (result["score"] / result["total"]) * 100
        history_data.append({
            "Date": result["date"],
            "Quiz": result["quiz_title"],
            "Topic": result["topic"],
            "Language": result["language"],
            "Difficulty": result["difficulty"],
            "Score": f"{result['score']}/{result['total']} ({percentage:.1f}%)"
        })
    
    # Sort by date, newest first
    history_data.sort(key=lambda x: x["Date"], reverse=True)
    
    df = pd.DataFrame(history_data)
    st.dataframe(df, use_container_width=True)
    
    # Some analytics
    if len(history_data) > 1:
        st.subheader("Your Progress")
        
        # Calculate average score by topic
        topic_data = {}
        for result in st.session_state.quiz_history:
            topic = result["topic"]
            if topic not in topic_data:
                topic_data[topic] = {"total": 0, "correct": 0, "count": 0}
            topic_data[topic]["correct"] += result["score"]
            topic_data[topic]["total"] += result["total"]
            topic_data[topic]["count"] += 1
        
        # Create chart data
        chart_data = []
        for topic, data in topic_data.items():
            percentage = (data["correct"] / data["total"]) * 100
            chart_data.append({
                "Topic": topic,
                "Percentage": percentage,
                "Quizzes Taken": data["count"]
            })
        
        # Display chart
        if chart_data:
            chart_df = pd.DataFrame(chart_data)
            st.bar_chart(chart_df.set_index("Topic")["Percentage"])
        
        # Clear history button
        if st.button("Clear History"):
            st.session_state.quiz_history = []
            # Also delete from disk
            if os.path.exists("quiz_history.json"):
                os.remove("quiz_history.json")
            st.success("History cleared!")
            st.rerun()

# --- Main App Logic ---
def main():
    # Load saved quizzes from disk on startup
    if 'saved_quizzes' not in st.session_state or not st.session_state.saved_quizzes:
        try:
            if os.path.exists("saved_quizzes.json"):
                with open("saved_quizzes.json", "r") as f:
                    st.session_state.saved_quizzes = json.load(f)
        except Exception:
            pass
    
    # Display the appropriate page
    if st.session_state.page == "create":
        show_create_quiz_page()
    elif st.session_state.page == "saved":
        show_saved_quizzes_page()
    elif st.session_state.page == "take" and st.session_state.quiz_in_progress:
        show_take_quiz_page()
    elif st.session_state.page == "history":
        show_history_page()
    else:
        show_create_quiz_page()

if __name__ == "__main__":
    main()