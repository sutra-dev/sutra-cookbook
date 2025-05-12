# 🌐 Multilingual Question Generator

A Streamlit application for creating educational questions in 50+ languages using the Sutra LLM from Two.ai and the Educhain framework.

## 🌟 Features

- **Rich Language Support**: Generate questions in 50+ languages including English, Hindi, Gujarati,  Bengali, Tamil, Telugu, and many international languages
- **Multiple Question Formats**: Create different types of questions including Multiple Choice, Short Answer, True/False, and Fill in the Blank
- **Customizable Generation**: Adjust number of questions and add custom instructions to tailor content
- **Educational Enhancement**: Includes explanations and correct answers with each question
- **Keyword Highlighting**: For short answer questions, provides relevant keywords to look for in answers
- **User-friendly Interface**: Simple and intuitive design for seamless content creation
- **Responsive Design**: Works well on both desktop and mobile devices
- **Pedagogical Focus**: Generate questions on any educational topic across different subjects

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Sutra API Key (from Two.ai)
- Educhain library

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/sutra-dev/sutra-cookbook.git
   cd Sutra_Cookbooks/starter-apps/Multilingual_Question_Generator
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
2. Select your preferred question type from the dropdown (Multiple Choice, Short Answer, True/False, Fill in the Blank)
3. Choose your target language from the 50+ available options
4. Adjust the number of questions using the slider (1-8)
5. Enter the educational topic you want to create questions for
6. Add any custom instructions to guide the content creation (optional)
7. Click "Generate Questions" to create your educational content
8. Review your questions, each including:
   - Question text
   - Options (for multiple choice)
   - Correct answer
   - Explanation of the answer
   - Keywords (for short answer questions)

## 📋 Question Types

The application supports four question formats:

- **Multiple Choice**:
  - Questions with several options
  - One correct answer identified
  - Explanation of why the answer is correct

- **Short Answer**:
  - Open-ended questions requiring brief responses
  - Sample answer provided
  - Keywords to look for in student responses

- **True/False**:
  - Statement-based questions
  - Binary correct answer (True or False)
  - Explanation of the correct determination

- **Fill in the Blank**:
  - Sentences with missing words or phrases
  - Correct terms to complete the sentences
  - Explanation of why the term fits

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
- Odia (ଓଡ଼ିଆ)
- Sanskrit (संस्कृत)
- Korean (한국어)
- Japanese (日本語)
- And 35+ more international languages

## 🎨 Technical Details

This application uses:
- **Streamlit** for the interactive web interface
- **Educhain** framework for educational content generation
- **Sutra LLM API** via LangChain for multilingual capability
- **Environment variables** for secure API key management
- **Caching mechanisms** for improved performance
- **Responsive design** for accessibility on various devices

## 🔒 Privacy & Security

- No personal user information is collected or stored
- API keys are securely managed using environment variables
- All content is generated on-demand without persistent storage

## 🎯 Target Users

- **Teachers and educators** creating assessment materials
- **Educational content creators** developing learning resources
- **Tutoring services** preparing practice questions
- **Students** practicing with diverse question formats
- **Language teachers** creating materials in native languages
- **Educational technology developers** integrating question generation

## 🌱 Key Benefits

- **Time Efficiency**: Quickly generate diverse question sets
- **Language Accessibility**: Create questions in learners' native languages
- **Assessment Variety**: Mix different question types for comprehensive evaluation
- **Pedagogical Quality**: Questions include explanations for better learning
- **Customization**: Tailor questions to specific educational needs
- **Subject Flexibility**: Generate questions across any academic discipline

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Educhain](https://github.com/satvik314/educhain) for the educational content framework
- [Sutra LLM](https://www.two.ai/sutra) for the powerful multilingual language model
- [Streamlit](https://streamlit.io) for the web application framework
- [LangChain](https://www.langchain.com) for the LLM integration
- [Python-dotenv](https://github.com/theskumar/python-dotenv) for environment variable management
