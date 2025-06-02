# 🌐 Global News Hub

A powerful multilingual news aggregation application that fetches the latest news from around the world and translates it into 50+ languages using AI-powered translation.

![Global News Hub](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **🔍 Real-time News Search**: Search for news on any topic using the Serper API
- **🌍 50+ Language Support**: Translate news articles into multiple languages including:
  - **Indian Languages**: Hindi, Gujarati, Bengali, Tamil, Telugu, Kannada, Malayalam, Punjabi, Marathi, Urdu, Assamese, Odia, Sanskrit
  - **Asian Languages**: Korean, Japanese, Chinese, Vietnamese, Thai, Indonesian, Malay, Tagalog
  - **European Languages**: French, German, Spanish, Portuguese, Russian, Italian, Dutch, Greek, Polish, Ukrainian, and more
  - **Others**: Arabic, Hebrew, Persian, Swahili, and many more

- **🖼️ High-Quality Images**: Automatically fetches relevant high-quality images for each news article
- **⚡ AI-Powered Translation**: Uses Sutra LLM for accurate and contextual translations
- **📱 Responsive Design**: Clean, modern interface that works on all devices
- **🔄 Real-time Processing**: Live translation with progress indicators
- **🎛️ Customizable Results**: Choose the number of articles to display (5-30)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Streamlit
- Required API keys (see API Keys section)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sutra-dev/sutra-cookbook.git
   cd sutra-cookbook/starter-apps/global-news-hub
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

## 🔑 API Keys

You'll need two API keys to use this application:

### 1. Serper API Key
- **Purpose**: Fetches news articles and images from Google News
- **Get your key**: [Serper.dev](https://serper.dev/)
- **Free tier**: 2,500 free searches per month
- **Features**: Real-time news search, image fetching

### 2. Sutra API Key
- **Purpose**: AI-powered translation of news articles
- **Get your key**: [SUTRA API](https://www.two.ai/sutra/api)
- **Model**: Sutra-v2 (High-quality multilingual LLM)
- **Features**: Accurate translation, context preservation

## 📦 Dependencies

```txt
streamlit>=1.28.0
requests>=2.31.0
langchain-openai>=0.0.2
langchain>=0.1.0
```

Create a `requirements.txt` file with these dependencies:

```bash
pip freeze > requirements.txt
```

## 🎯 How to Use

1. **Enter API Keys**
   - Add your Serper API key in the sidebar
   - Add your Sutra API key in the sidebar

2. **Search for News**
   - Enter any search term (e.g., "artificial intelligence", "climate change", "sports")
   - Click the "Search" button

3. **Choose Language**
   - Select your preferred language from the dropdown
   - The app will automatically translate the news

4. **Customize Results**
   - Adjust the number of articles using the slider (5-30)
   - Each article includes title, source, description, and image

## 🏗️ Architecture

```
Global News Hub
├── News Search (Serper API)
│   ├── Query Translation
│   ├── News Fetching
│   └── Image Enhancement
├── AI Translation (Sutra LLM)
│   ├── Context-Aware Translation
│   ├── Cultural Adaptation
│   └── Proper Noun Preservation
└── User Interface (Streamlit)
    ├── Responsive Layout
    ├── Real-time Updates
    └── Interactive Controls
```

## 🛠️ Technical Details

### Translation Process
- **Query Translation**: Non-English queries are first translated to English for better search results
- **Content Translation**: News articles are translated while preserving:
  - Proper nouns (names, places)
  - Numbers and dates
  - Technical terms
  - Cultural context

### Image Enhancement
- Fetches high-quality images using Serper Images API
- Responsive image display with fixed aspect ratios
- Fallback handling for missing images

### Performance Optimizations
- **Caching**: LLM model instances are cached for better performance
- **Streaming**: Real-time translation progress updates
- **Batch Processing**: Efficient handling of multiple articles

## 🎨 UI/UX Features

- **Modern Design**: Clean, card-based layout
- **Responsive Columns**: Optimal text-to-image ratio
- **Visual Feedback**: Loading spinners and progress indicators
- **Error Handling**: Graceful fallbacks and user-friendly error messages
- **Accessibility**: Proper semantic markup and contrast

## 🔧 Configuration

### Environment Variables (Optional)
```bash
export SERPER_API_KEY="your_serper_key_here"
export SUTRA_API_KEY="your_sutra_key_here"
```

### Customization Options
- **Temperature Setting**: Adjust translation creativity (default: 0.3)
- **Result Limits**: Configure max articles per search
- **Language Mappings**: Add or modify supported languages


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Serper.dev** - For providing excellent news search API
- **Two.ai** - For the powerful Sutra LLM translation capabilities
- **Streamlit** - For the amazing web app framework
- **LangChain** - For LLM integration utilities