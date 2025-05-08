# 🌐 Sutra Multilingual Chatbot

A Streamlit application that enables conversations in 50+ languages using the powerful Sutra LLM API from Two.ai.

## 🌟 Features

- **Extensive Language Support**: Chat in 50+ languages including Hindi, English, Gujarati, Bengali, Tamil, Telugu, French, Chinese, Arabic, and many more
- **Real-time Streaming**: Experience fluid conversations with streaming responses
- **User-friendly Interface**: Clean, intuitive UI with dark mode support
- **Conversation History**: Review your complete chat history within the session
- **Responsive Design**: Works well on desktop and mobile devices
- **Customizable**: Select your preferred language from the sidebar
- **Fast Performance**: Optimized for quick responses and smooth user experience
- **Error Handling**: Robust error management for API issues and edge cases

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Sutra API Key (from Two.ai)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Shubhwithai/Sutra_Cookbooks.git
   cd Sutra_Cookbooks/starter-apps/Sutra-Multilingual-Chat
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

1. Select your preferred language from the sidebar dropdown menu
2. Type your message in the chat input box at the bottom
3. View the AI's response in real-time with streaming text
4. Continue the conversation naturally with follow-up questions
5. Switch languages anytime using the sidebar selector

## 📋 Technical Details

This application uses:
- **Streamlit** for the web interface and state management
- **Sutra LLM API** via LangChain framework for multilingual text generation
- **Callbacks** for streaming responses in real-time 
- **Environment variables** for secure API key management
- **Exception handling** for robust error management
- **Caching** for improved performance with resource-intensive operations

## 🌍 Supported Languages

The application supports 50+ languages including:
- English, Hindi, Gujarati, Bengali, Tamil
- Telugu, Kannada, Malayalam, Punjabi, Marathi
- Urdu, Assamese, Odia, Sanskrit, Korean
- Japanese, Arabic, French, German, Spanish
- Portuguese, Russian, Chinese, Vietnamese, Thai
- Indonesian, Turkish, Polish, Ukrainian, Dutch
- And many more!

## 🔒 Privacy & Security

- No conversation data is stored beyond your current session
- API keys are securely managed using environment variables
- No personal information is collected or transmitted

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Sutra LLM](https://www.two.ai/sutra) for the powerful multilingual language model
- [Streamlit](https://streamlit.io) for the web application framework
- [LangChain](https://www.langchain.com) for the LLM integration
- [Python-dotenv](https://github.com/theskumar/python-dotenv) for environment variable management
