# 🏛️ Government Scheme Explainer

A Streamlit application that explains Indian government schemes in multiple regional languages using the Sutra LLM  from Two.ai.

## 🌟 Features

- **Multilingual Support**: Access scheme information in 13 Indian languages including Hindi, Gujarati, Bengali, Tamil, Telugu, and more
- **Comprehensive Scheme Database**: Covers 40+ government schemes across 8 major categories
- **Personalized Explanations**: Customize explanation depth for benefits, eligibility, and application processes
- **User-Centric Design**: Tailor information based on education level, location, and prior knowledge
- **Real-time Streaming**: Experience fluid conversations with streaming responses
- **Interactive UI**: Clean interface with category-based navigation and visual enhancements
- **Example Integration**: Optional inclusion of practical examples and case studies
- **Scheme Comparison**: Optional comparison between similar government programs
- **Full Conversation History**: Review your complete chat session

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Sutra API Key (from Two.ai)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/sutra-dev/sutra-cookbook.git
   cd Sutra_Cookbooks/starter-apps/Government_Scheme_Explainer
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

1. Select your preferred language from the sidebar dropdown menu (includes native script names)
2. Choose a scheme category (Agriculture, Housing, Health, Education, etc.)
3. Select a specific government scheme
4. Customize your explanation preferences:
   - Adjust detail levels for benefits, eligibility, and application process
   - Choose whether to include examples and scheme comparisons
   - Set your user profile (education level, scheme familiarity, location type)
5. Ask questions about the scheme in the chat input
6. View AI-generated explanations tailored to your preferences

## 📋 Scheme Categories

The application covers schemes in 8 major categories:
- **👨‍🌾 Agriculture & Rural**: PM-KISAN, Kisan Credit Card, MGNREGA, etc.
- **🏠 Housing & Urban**: Pradhan Mantri Awas Yojana, Smart Cities Mission, etc.
- **🏥 Health & Wellness**: Ayushman Bharat, PM Jan Arogya Yojana, etc.
- **👩‍🎓 Education & Skills**: Samagra Shiksha, PM POSHAN, Skill India Mission, etc.
- **💼 Employment & Entrepreneurship**: PM Mudra Yojana, Startup India, etc.
- **👵 Social Security & Pension**: Atal Pension Yojana, PM Vaya Vandana Yojana, etc.
- **💡 Energy & Infrastructure**: Saubhagya, Ujjwala Yojana, PM Gram Sadak Yojana, etc.
- **🏦 Financial Inclusion**: Jan Dhan Yojana, Digital India, BHIM UPI, etc.

## 🌍 Supported Languages

The application supports 13 Indian languages:
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

## 🎨 Technical Details

This application uses:
- **Streamlit** for the interactive web interface
- **Sutra LLM API** via LangChain for multilingual text generation
- **Custom UI components** for enhanced visual experience
- **Streaming responses** for real-time information delivery
- **Dynamic context building** based on user preferences
- **Environment variables** for secure API key management

## 🔒 Privacy & Security

- No personal information is collected or stored
- No tracking of user queries beyond the current session
- API keys are securely managed using environment variables
- All explanations are generated on-demand without persistent storage

## 🎯 Use Cases

- **Citizens** seeking information about government schemes
- **Gram panchayat** and community leaders helping local populations
- **NGOs** working on citizen awareness programs
- **Government officials** explaining schemes to constituents
- **Students** researching government welfare programs
- **Social workers** assisting beneficiaries with applications

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Sutra LLM](https://www.two.ai/sutra) for the powerful multilingual language model
- [Streamlit](https://streamlit.io) for the web application framework
- [LangChain](https://www.langchain.com) for the LLM integration
- [Python-dotenv](https://github.com/theskumar/python-dotenv) for environment variable management
- Government of India for public information on schemes
