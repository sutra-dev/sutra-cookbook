# 🌾 Krishi Mitra (कृषि मित्र) - Farmer Assistant

A Streamlit application providing  personalized agricultural advice to farmers in 13 Indian languages using the Sutra LLM from Two.ai.

## 🌟 Features

- **Multilingual Support**: Access farming advice in 13 Indian languages including Hindi, Gujarati, Bengali, Tamil, Telugu, and more
- **Comprehensive Agricultural Knowledge**: Covers 40+ specific farming topics across 8 major categories
- **Customizable Advice**: Adjust detail levels and content focus based on farmer needs
- **Traditional & Scientific Balance**: Option to include both local farming practices and scientific information
- **Practical Guidance**: Actionable steps with safety precautions and sustainable alternatives
- **Real-time Streaming**: Experience fluid conversations with streaming responses
- **User-friendly Interface**: Simple navigation with category-based topic selection
- **Responsive Design**: Works well on both desktop and mobile devices
- **Complete Chat History**: Review your entire conversation within the session

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Sutra API Key (from Two.ai)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/sutra-dev/sutra-cookbook.git
   cd Sutra_Cookbooks/starter-apps/Farmer_Assistant
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
2. Choose a main agricultural category (Crop Management, Irrigation, etc.)
3. Select a specific topic within the chosen category
4. Customize your advice preferences (optional):
   - Adjust detail level using the response detail slider
   - Toggle inclusion of local farming practices
   - Toggle inclusion of scientific information
5. Ask questions about the selected topic in the chat input
6. Receive tailored agricultural advice in your chosen language

## 📋 Agricultural Categories

The application covers farming topics in 8 major areas:

- **🌱 Crop Management**: Seed selection, crop rotation, intercropping, spacing, harvesting
- **💧 Irrigation**: Drip systems, sprinklers, water conservation, watering schedules, rainwater harvesting
- **🐛 Pest Management**: Organic control, pest identification, integrated management, natural predators
- **🌿 Organic Farming**: Compost preparation, natural fertilizers, certification, soil health
- **🧪 Soil Health**: Testing methods, pH balancing, nutrient management, conservation
- **💲 Farm Economics**: Cost reduction, market rates, government schemes, crop insurance
- **🚜 Farm Equipment**: Selection, maintenance, modern tools, cost-effective alternatives
- **🌧️ Weather Advisory**: Seasonal forecasts, weather-based planting, climate resilience

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
- **Sutra LLM API** via LangChain for multilingual agricultural advice
- **Streaming response technology** for real-time information delivery
- **Dynamic context building** based on selected topics and preferences
- **Environment variables** for secure API key management
- **Responsive design** for accessibility on various devices

## 🔒 Privacy & Security

- No personal farmer information is collected or stored
- No tracking of queries beyond the current session
- API keys are securely managed using environment variables
- All advice is generated on-demand without persistent storage

## 🎯 Target Users

- **Small and marginal farmers** seeking accessible agricultural information
- **Agricultural extension workers** assisting farmers with technical advice
- **Rural development organizations** working with farming communities
- **Agricultural colleges and universities** for demonstration purposes
- **Farmer producer organizations (FPOs)** supporting member farmers
- **Agri-businesses** providing support to their farmer networks

## 🌱 Key Benefits

- **Knowledge Accessibility**: Makes agricultural expertise available in regional languages
- **Cost Reduction**: Helps farmers optimize resources and reduce expenses
- **Sustainability**: Promotes sustainable farming practices and alternatives
- **Productivity**: Improves crop yields through better management practices
- **Risk Management**: Provides guidance on pest control and weather adaptation
- **Digital Inclusion**: Bridges the digital divide in agricultural information

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Sutra LLM](https://www.two.ai/sutra) for the powerful multilingual language model
- [Streamlit](https://streamlit.io) for the web application framework
- [LangChain](https://www.langchain.com) for the LLM integration
- [Python-dotenv](https://github.com/theskumar/python-dotenv) for environment variable management
- Agricultural research institutions for publicly available farming information
