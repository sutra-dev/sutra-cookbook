# 🛍️ Multilingual Shopping Hub

A powerful multilingual e-commerce search application that allows users to search for products from around the world and view results in 50+ languages. Built with Streamlit, powered by Serper API for product search and Sutra LLM for intelligent translation.

![Multilingual Shopping Hub](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)


## ✨ Features

- **🌍 Global Product Search**: Search for products from major e-commerce platforms worldwide
- **🗣️ 50+ Language Support**: Translate product information into any of 50+ supported languages
- **🎯 Smart Filtering**: Filter products by price range and customize result count
- **🖼️ High-Quality Images**: Enhanced product images for better visual experience
- **⭐ Rich Product Details**: View ratings, prices, delivery info, and store information
- **🌙 Theme Support**: Automatic light/dark theme compatibility
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Streamlit
- API keys for Serper and Sutra services

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sutra-dev/sutra-cookbook.git
   cd sutra-cookbook/starter-apps/multilingual-shopping-hub
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
   Navigate to `http://localhost:8501`

## 🔑 API Keys Setup

### Serper API Key
1. Visit [Serper.dev](https://serper.dev/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Enter it in the sidebar of the application

### Sutra API Key
1. Visit [SUTRA API](https://www.two.ai/sutra/api)
2. Sign up for a free account
3. Get your API key
4. Enter it in the sidebar for translation features

## 📦 Dependencies

```txt
streamlit
requests
langchain-openai
langchain
json
```

Create a `requirements.txt` file with:
```txt
streamlit>=1.28.0
requests>=2.31.0
langchain-openai>=0.1.0
langchain>=0.1.0
```

## 🌐 Supported Languages

The application supports translation into 50+ languages including:

**Asian Languages**: Hindi, Gujarati, Bengali, Tamil, Telugu, Kannada, Malayalam, Punjabi, Marathi, Urdu, Assamese, Odia, Sanskrit, Korean, Japanese, Chinese, Vietnamese, Thai, Indonesian, Malay, Tagalog

**European Languages**: French, German, Spanish, Portuguese, Russian, Italian, Greek, Polish, Ukrainian, Dutch, Hebrew, Persian, Swedish, Norwegian, Danish, Finnish, Czech, Hungarian, Romanian, Bulgarian, Croatian, Serbian, Slovak, Slovenian, Estonian, Latvian, Lithuanian

**Other Languages**: Arabic, Turkish, Swahili

## 🛠️ Usage

### Basic Search
1. Enter your API keys in the sidebar
2. Type your search query in the search bar
3. Click "Search" to fetch products
4. Browse through the results

### Advanced Features
- **Language Selection**: Choose your preferred language from the dropdown
- **Price Filtering**: Set minimum and maximum price limits
- **Result Count**: Adjust how many products to display (5-30)
- **Smart Translation**: Queries in non-English languages are automatically translated for better search results

### Search Tips
- Use specific product names for better results
- Include brand names when searching
- Try different keyword combinations
- Use price filters to narrow down options

## 🎨 Features in Detail

### Product Information Display
Each product card shows:
- **Product Title**: Translated product name
- **Store Information**: Retailer/marketplace name
- **Price**: Current product price
- **Delivery Info**: Shipping and delivery details
- **Ratings**: Star ratings and review counts
- **High-Quality Images**: Enhanced product photos
- **Direct Links**: Quick access to product pages

### Smart Translation
- Automatic query translation to English for optimal search results
- Product information translated to selected language
- Preserves brand names, technical specifications, and pricing
- Maintains cultural appropriateness for target language

### Responsive Design
- Adapts to different screen sizes
- Optimized for both desktop and mobile viewing
- Theme-aware styling (light/dark mode support)
- Accessible design with proper contrast ratios

## 🔧 Configuration

### Customizing Search Parameters
```python
# In the sidebar, you can adjust:
- Number of results: 5-30 products
- Price range: $0-$10,000
- Language selection: 50+ languages
```

### API Rate Limits
- **Serper API**: Check your plan limits on Serper.dev
- **Sutra API**: Check your usage limits on two.ai


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Serper API** for providing comprehensive product search capabilities
- **Sutra LLM** for intelligent multilingual translation
- **Streamlit** for the amazing web app framework
- **LangChain** for LLM integration utilities