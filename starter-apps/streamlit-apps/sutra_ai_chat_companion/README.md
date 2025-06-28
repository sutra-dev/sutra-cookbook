# SUTRA AI Friend Chatbot 🔗

An intelligent AI friend and mentor chatbot built with Streamlit, featuring multi-language support, memory capabilities, and web search functionality.

![SUTRA AI](https://framerusercontent.com/images/3Ca34Pogzn9I3a7uTsNSlfs9Bdk.png)

## ✨ Features

- **Multi-language Support**: Chat in English, Hindi, Marathi, Gujarati, Tamil, Telugu, Kannada, Punjabi, and Bihari
- **Memory Integration**: Persistent conversation memory using Mem0 API
- **Web Search**: Real-time information retrieval through DuckDuckGo integration
- **Modern UI**: Dark theme with responsive design
- **AI Agent Framework**: Powered by Agno agents with fallback API support
- **Translation**: Automatic language translation for memory storage

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Streamlit
- SUTRA API key from [Two AI](https://two.ai/)
- Mem0 API key (optional) from [Mem0.ai](https://mem0.ai/)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd sutra-ai-chatbot
```

2. **Install dependencies**
```bash
pip install streamlit requests
```

3. **Install optional dependencies** (for enhanced features)
```bash
# For memory functionality
pip install mem0ai

# For agent framework and web search
pip install agno openai

# For translation
pip install googletrans==4.0.0rc1
```

4. **Add your logo**
Place your logo file as `logo_bg.png` in the project directory.

5. **Run the application**
```bash
streamlit run app.py
```

## 🔧 Configuration

### Required API Keys

1. **SUTRA API Key** (Required)
   - Get from [Two AI Sutra](https://two.ai/)
   - Format: `sutra_xxxxxxxxxxxxxx`

2. **Mem0 API Key** (Optional)
   - Get from [Mem0.ai](https://mem0.ai/)
   - Format: `m0-xxxxxxxxxxxxxx`
   - Enables conversation memory and context

### Environment Setup

The application will automatically set environment variables for:
- `SUTRA_API_KEY`
- `MEM0_API_KEY`

## 📋 Dependencies

### Core Dependencies
```
streamlit
requests
```

### Optional Dependencies
```
mem0ai          # Memory functionality
agno           # AI agent framework
openai         # OpenAI-compatible API client
googletrans    # Language translation
```

## 🎯 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Configure API keys**
   - Enter your SUTRA API key in the sidebar
   - Optionally add Mem0 API key for memory features

3. **Select language**
   - Choose from 9 supported languages in the sidebar

4. **Start chatting**
   - Type your message in the chat input
   - Sutra will respond with contextual, empathetic replies

## 🏗️ Architecture

### Core Components

- **Streamlit Frontend**: Modern dark UI with responsive design
- **SUTRA AI Model**: Primary language model via Two AI API
- **Agno Agent Framework**: Enhanced AI capabilities with tool integration
- **Mem0 Memory**: Persistent conversation context
- **Translation Layer**: Multi-language support

### Fallback System

The application implements a robust fallback system:
1. **Primary**: Agno agent with DuckDuckGo tools
2. **Fallback**: Direct SUTRA API calls
3. **Error Handling**: Graceful degradation for missing dependencies

## 🎨 UI Features

- **Dark Theme**: Modern black and blue color scheme
- **Responsive Design**: Optimized for different screen sizes
- **Chat Bubbles**: User and assistant message differentiation
- **Loading States**: Visual feedback during API calls
- **Sidebar Configuration**: Compact API and language settings

## 🔍 Technical Details

### Memory System
- Stores conversations in English for consistency
- Retrieves context from last 30 days
- Automatic translation for non-English inputs

### Agent Configuration
- **Name**: AIMentor
- **Personality**: Empathetic AI friend from Pune, India
- **Tools**: DuckDuckGo web search
- **Model**: SUTRA-v2 via Two AI API

### Error Handling
- Network timeout protection (30s)
- API error responses with status codes
- Graceful fallback for missing dependencies
- Translation error handling

## 🌐 Supported Languages

- English
- Hindi (हिंदी)
- Marathi (मराठी)
- Gujarati (ગુજરાતી)
- Tamil (தமிழ்)
- Telugu (తెలుగు)
- Kannada (ಕನ್ನಡ)
- Punjabi (ਪੰਜਾਬੀ)
- Bihari (भोजपुरी)

## 🛠️ Customization

### Styling
Modify the CSS in the `st.markdown()` section to customize:
- Colors and themes
- Layout and spacing
- Font families
- Component styling

### Agent Personality
Update the agent instructions in the `mentor_agent` configuration:
```python
instructions=[
    "You are Sutra, an AI friend and mentor...",
    "Customize personality traits here...",
]
```

### Memory Settings
Adjust memory retention period:
```python
if now - mem_time < timedelta(days=30):  # Change days as needed
```

## 🔒 Security

- API keys are handled securely through Streamlit's password input
- No API keys are stored in code or session state
- Memory data is user-scoped with unique USER_ID

## 📱 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
1. **Streamlit Cloud**: Connect your GitHub repository
2. **Docker**: Create Dockerfile with dependencies
3. **Heroku**: Use requirements.txt for dependencies

### Environment Variables
For production, set environment variables:
- `SUTRA_API_KEY`
- `MEM0_API_KEY`

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Install optional dependencies as needed
   - Application gracefully handles missing packages

2. **API Errors**
   - Verify API key format and validity
   - Check network connectivity
   - Review API usage limits

3. **Memory Issues**
   - Ensure Mem0 API key is valid
   - Check memory search permissions

4. **Translation Errors**
   - Falls back to original text if translation fails
   - Install `googletrans==4.0.0rc1` for stability

## 📄 License

[Add your license information here]

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation
- Contact support through respective API providers

---

Made with ❤️ using Streamlit and SUTRA AI