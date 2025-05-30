# 📰 Regional Language News Summarizer

A Streamlit application that summarizes news articles in 50+ languages using the powerful Sutra LLM API from Two.ai.

## 🌟 Features

- **Extensive Language Support**:  Summarize news in 50+ languages including Hindi, English, Gujarati, Bengali, Tamil, Telugu, French, Chinese, Arabic, and many more
- **Real-time Streaming**: Experience fluid summarization with streaming responses
- **Multiple Input Options**: Paste text, upload files (TXT, PDF, MD), or provide a URL
- **Customizable Outputs**: Tailor summaries with different lengths, styles, and focus areas
- **Smart Content Extraction**: Automatically pulls article content from URLs
- **PDF Support**: Extract and process text from PDF documents
- **Translation Capability**: Translate summaries between any of the supported languages
- **Comprehensive History**: Keep track of all generated summaries with options to regenerate or download
- **Batch Download**: Download all your summaries at once
- **Text Preprocessing**: Clean whitespace, remove URLs, and strip HTML tags
- **Responsive Design**: Works well on desktop and mobile devices

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Sutra API Key (from Two.ai)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/sutra-dev/sutra-cookbook.git
   cd Sutra_Cookbooks/starter-apps/Regional_News_Summarizer
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

1. Choose your input method (text, file, or URL) on the Summarize News tab
2. Configure your summarization preferences in the sidebar:
   - Source language of the article
   - Target language for the summary
   - Summary length (Very Short to Comprehensive)
   - Style (Neutral, Simplified, Academic, Conversational, Bullet Points)
   - Focus areas (Key Facts, Statistics, Quotes, etc.)
   - Advanced options for text preprocessing
3. Click "Generate Summary" to process your news content
4. View, save, regenerate, or translate your summaries in the History tab
5. Download individual summaries or export your entire history

## 📋 Technical Details

This application uses:
- **Streamlit** for the web interface and state management
- **Sutra LLM API** via LangChain framework for multilingual text generation and translation
- **BeautifulSoup** for web scraping and HTML processing
- **PyPDF2** for extracting text from PDF documents
- **Callbacks** for streaming responses in real-time 
- **Environment variables** for secure API key management
- **Exception handling** for robust error management

## 🌍 Supported Languages

The application supports 50+ languages including:
- English, Hindi, Gujarati, Bengali, Tamil
- Telugu, Kannada, Malayalam, Punjabi, Marathi
- Urdu, Assamese, Odia, Sanskrit, Korean
- Japanese, Arabic, French, German, Spanish
- Portuguese, Russian, Chinese, Vietnamese, Thai
- Indonesian, Turkish, Polish, Ukrainian, Dutch
- And many more!

## 📊 Summary Customization Options

### Length Options:
- Very Short: Key points only (1-2 sentences)
- Short: Brief overview (3-4 sentences)
- Medium: Standard summary (1-2 paragraphs)
- Detailed: Comprehensive coverage (3-4 paragraphs)
- Comprehensive: In-depth analysis (5+ paragraphs)

### Style Options:
- Neutral: Balanced and objective reporting
- Simplified: Easy-to-understand language
- Academic: Formal and analytical tone
- Conversational: Casual and engaging style
- Bullet Points: Organized as concise bullet points

### Focus Areas:
- Key Facts: Essential information
- Statistics: Numerical data and figures
- Quotes: Important statements from sources
- Background Context: Historical or situational context
- Future Implications: Potential outcomes or consequences

## 🔒 Privacy & Security

- No article or summary data is stored beyond your current session
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
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping
- [PyPDF2](https://pypdf2.readthedocs.io/) for PDF processing
- [Python-dotenv](https://github.com/theskumar/python-dotenv) for environment variable management
