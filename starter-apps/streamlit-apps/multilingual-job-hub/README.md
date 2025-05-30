# 💼 Multilingual Job Hub

A powerful job search application that fetches real-time job listings from around the world and translates them into 50+ languages using AI-powered translation. Find your dream job in any language!

![Job Hub](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![SerpAPI](https://img.shields.io/badge/SerpAPI-Integrated-green.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **🔍 Global Job Search**: Search for jobs worldwide using SerpAPI's Google Jobs integration
- **🌍 50+ Language Support**: Translate job listings into multiple languages including:
  - **Indian Languages**: Hindi, Gujarati, Bengali, Tamil, Telugu, Kannada, Malayalam, Punjabi, Marathi, Urdu, Assamese, Odia, Sanskrit
  - **Asian Languages**: Korean, Japanese, Chinese, Vietnamese, Thai, Indonesian, Malay, Tagalog
  - **European Languages**: French, German, Spanish, Portuguese, Russian, Italian, Dutch, Greek, Polish, Ukrainian, and more
  - **Others**: Arabic, Hebrew, Persian, Swahili, and many more

- **🏢 Company Logos**: Automatically fetches high-quality company logos for each job listing
- **🌎 Location-Based Search**: Filter jobs by specific countries (India, Mexico, Japan, Germany, France, Brazil, Indonesia)
- **⚡ AI-Powered Translation**: Uses Sutra LLM for accurate and contextual job description translations
- **📱 Responsive Design**: Modern, card-based interface with dark/light theme support
- **🔄 Real-time Processing**: Live translation with progress indicators
- **🎯 Job-Specific Translations**: Preserves technical terms, skills, and requirements accuracy

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Streamlit
- Required API keys (see API Keys section)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sutra-dev/sutra-cookbook.git
   cd sutra-cookbook/starter-apps/multilingual-job-hub
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

### 1. SerpAPI Key
- **Purpose**: Fetches job listings and company logos from Google Jobs
- **Get your key**: [SerpAPI Registration](https://serpapi.com/users/sign_in)
- **Free tier**: 100 free searches per month
- **Features**: Real-time job search, company logo fetching, location filtering

### 2. Sutra API Key
- **Purpose**: AI-powered translation of job listings and descriptions
- **Get your key**: [SUTRA API](https://www.two.ai/sutra/api)
- **Model**: Sutra-v2 (High-quality multilingual LLM)
- **Features**: Accurate translation, technical term preservation, context awareness

## 📦 Dependencies

Create a `requirements.txt` file with these dependencies:

```txt
streamlit>=1.28.0
requests>=2.31.0
langchain-openai>=0.0.2
langchain>=0.1.0
google-search-results>=2.4.2
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

## 🎯 How to Use

1. **Enter API Keys**
   - Add your SerpAPI key in the sidebar
   - Add your Sutra API key in the sidebar

2. **Search for Jobs**
   - Enter job search terms (e.g., "Python Developer", "Data Scientist", "Marketing Manager")
   - Select your preferred location from the dropdown
   - Click the "Search" button

3. **Choose Language**
   - Select your preferred language from the dropdown (50+ options available)
   - The app will automatically translate job listings

4. **Browse Results**
   - View job titles, company names, locations, and descriptions
   - See company logos for visual identification
   - Click "View Job" links to apply directly

## 🏗️ Architecture

```
Multilingual Job Hub
├── Job Search (SerpAPI)
│   ├── Google Jobs Integration
│   ├── Company Logo Fetching
│   └── Location-Based Filtering
├── AI Translation (Sutra LLM)
│   ├── Query Translation
│   ├── Job Description Translation
│   ├── Technical Term Preservation
│   └── Cultural Adaptation
└── User Interface (Streamlit)
    ├── Responsive Card Layout
    ├── Theme-Aware Design
    ├── Real-time Updates
    └── Interactive Controls
```

## 🛠️ Technical Features

### Translation Process
- **Query Translation**: Non-English job searches are translated to English for better results
- **Content Translation**: Job listings are translated while preserving:
  - Technical skills and requirements
  - Company names (with cultural adaptations)
  - Job titles and industry terminology
  - Location information
  - Salary and benefit details

### Company Logo Enhancement
- Automatically fetches high-quality company logos using Google Images
- Responsive logo display with proper aspect ratios
- Fallback handling for companies without available logos
- Optimized loading and caching

### Performance Optimizations
- **Model Caching**: LLM instances are cached for better performance
- **Batch Processing**: Efficient handling of multiple job translations
- **Error Recovery**: Graceful fallbacks when translation fails
- **Rate Limiting**: Proper API usage management

## 🎨 UI/UX Features

### Modern Design
- **Card-Based Layout**: Clean, professional job cards
- **Theme Support**: Automatic dark/light theme detection
- **Responsive Design**: Works perfectly on desktop and mobile
- **Visual Hierarchy**: Clear information organization

### Interactive Elements
- **Real-time Search**: Instant job fetching and translation
- **Progress Indicators**: Visual feedback during processing
- **Error Handling**: User-friendly error messages
- **Loading States**: Professional loading animations

### Accessibility
- **Semantic HTML**: Proper markup for screen readers
- **Contrast Compliance**: Meets accessibility standards
- **Keyboard Navigation**: Full keyboard support
- **Multi-language Support**: Right-to-left language support

## 🌍 Supported Locations

- **India** - Comprehensive job market coverage
- **Mexico** - Latin American opportunities
- **Japan** - Asian market jobs
- **Germany** - European Union positions
- **France** - French-speaking market
- **Brazil** - South American opportunities
- **Indonesia** - Southeast Asian jobs

## 🔧 Configuration

### Environment Variables (Optional)
```bash
export SERP_API_KEY="your_serpapi_key_here"
export SUTRA_API_KEY="your_sutra_key_here"
```

### Customization Options
- **Translation Temperature**: Adjust creativity vs accuracy (default: 0.3)
- **Result Limits**: Configure maximum jobs per search
- **Language Mappings**: Add or modify supported languages
- **Location Filters**: Customize available search locations

## 🔍 Advanced Search Features

### Job Type Filtering
- Full-time positions
- Part-time opportunities
- Contract work
- Remote jobs
- Internships

### Smart Query Processing
- Automatic job-related keyword enhancement
- Skill-based search optimization
- Location-aware result filtering
- Industry-specific search improvements


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SerpAPI** - For providing excellent job search API integration
- **Two.ai** - For the powerful Sutra LLM translation capabilities
- **Streamlit** - For the amazing web application framework
- **LangChain** - For LLM integration and management utilities
- **Google Jobs** - For comprehensive job listing data