# 🌐 Professional Flashcard Studio - Multilingual Flashcard Generator

A Streamlit application for creating high-quality, educational flashcards in 50+ languages using the Sutra LLM from Two.ai.

## 🌟 Features

- **Extensive Language Support**: Generate  flashcards in 50+ languages including English, Hindi, Gujarati, Bengali, Tamil, Telugu, and many international languages
- **Professional-Grade Content**: Creates industry-standard educational flashcards with clear structure and academic precision
- **Customizable Generation**: Adjust the number of flashcards and add custom instructions for tailored content
- **Comprehensive Learning Structure**: Balanced coverage of foundational concepts, terminology, processes, and advanced applications
- **Educational Enhancement**: Includes explanations, examples, and learning aids with each flashcard
- **User-friendly Interface**: Simple and intuitive design for seamless content creation
- **Responsive Design**: Works well on both desktop and mobile devices
- **Learning Progression**: Flashcards organized in logical learning sequence from fundamental to complex concepts

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Sutra API Key (from Two.ai)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/sutra-dev/sutra-cookbook.git
   cd Sutra_Cookbooks/starter-apps/Professional_Flashcard_Studio
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API key:
   - Create a `.env` file with your Sutra API key:
     ```
     SUTRA_API_KEY=your_api_key_here
     ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## 💡 How to Use

1. Enter your Sutra API Key in the sidebar (if not set as an environment variable)
2. Select your preferred language from the dropdown menu
3. Adjust the number of flashcards using the slider (1-8)
4. Add any custom instructions to guide the content creation (optional)
5. Enter the educational topic you want to create flashcards for
6. Click "Generate Professional Flashcards"
7. Review your flashcards which include:
   - Front: Clear, concise questions or key terms
   - Back: Complete yet focused answers or definitions
   - Explanation: Additional context with examples or applications

## 📋 Flashcard Structure

Each generated flashcard set follows professional educational standards with:

- **Front Side**:
  - Clear, concise questions or key terms
  - Properly formatted technical terminology
  - Specific concept questions
  - Problem-solving scenarios

- **Back Side**:
  - Complete yet concise answers
  - Accurate definitions
  - Problem solutions with critical steps
  - Structured multi-part answers when needed

- **Explanation**:
  - Additional context for deeper understanding
  - Examples and applications
  - Connections to related concepts
  - Mnemonics and learning strategies

## 🌍 Supported Languages

The application supports 50+ languages including:
- English
- Hindi (हिन्दी)
- Gujarati (ગુજરાતી)
- Bengali (বাংলা)
- Tamil (தமிழ்)
- Telugu (తెలుగు)
- Kannada (ಕನ್ನಡ)
- Malayalam (മലയാളം)
- Punjabi (ਪੰਜਾਬੀ)
- Marathi (मराठी)
- Urdu (اردو)
- Assamese (অসমীয়া)
- Sanskrit (संस्कृत)
- Korean (한국어)
- Japanese (日本語)
- And 35+ more international languages

## 🎨 Technical Details

This application uses:
- **Streamlit** for the interactive web interface
- **Sutra LLM API** via LangChain for multilingual content generation
- **Pydantic** for structured data validation and parsing
- **Environment variables** for secure API key management
- **JSON formatting** for structured output handling
- **Responsive design** for accessibility on various devices

## 🔒 Privacy & Security

- No personal user information is collected or stored
- API keys are securely managed using environment variables
- All content is generated on-demand without persistent storage

## 🎯 Target Users

- **Teachers and educators** creating learning materials
- **Students** preparing for examinations
- **Language learners** studying vocabulary and concepts
- **Academic institutions** developing educational resources
- **Tutoring services** creating teaching aids
- **Self-learners** studying specialized topics

## 🌱 Key Benefits

- **Content Accessibility**: Creates educational content in many languages
- **Time Efficiency**: Quickly generates high-quality flashcards
- **Learning Optimization**: Structures content for effective knowledge retention
- **Consistency**: Ensures professional-grade educational content
- **Customization**: Adapts to specific learning needs through custom instructions
- **Multilingual Support**: Bridges language barriers in educational content

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Sutra LLM](https://www.two.ai/sutra) for the powerful multilingual language model
- [Streamlit](https://streamlit.io) for the web application framework
- [LangChain](https://www.langchain.com) for the LLM integration
- [Python-dotenv](https://github.com/theskumar/python-dotenv) for environment variable management
- [Educhain](https://github.com/satvik314/educhain) for the application framework
