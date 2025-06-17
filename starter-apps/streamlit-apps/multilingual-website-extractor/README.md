# Multilingual Website Data Extractor 🌐

A powerful Streamlit application that allows you to chat with website content in multiple languages using the SUTRA AI model.

## Features ✨

- **Multi-URL Support**: Analyze multiple websites simultaneously
- **50+ Languages**: Support for major world languages including English, Hindi, Gujarati, Bengali, Tamil, Telugu, Arabic, Chinese, Japanese, and many more
- **Intelligent Translation**: Automatic language detection and translation
- **Interactive Chat**: Ask questions about website content in any supported language
- **Real-time Processing**: Get instant responses from website data
- **User-friendly Interface**: Clean, intuitive Streamlit interface

## Supported Languages 🗣️

The app supports 50+ languages including:
- **Indian Languages**: Hindi, Gujarati, Bengali, Tamil, Telugu, Kannada, Malayalam, Punjabi, Marathi, Urdu, Assamese, Odia, Sanskrit
- **International Languages**: English, Spanish, French, German, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, and many more

## Prerequisites 📋

Before running the application, make sure you have:

1. Python 3.8 or higher
2. A SUTRA API key (get it free from [SUTRA API](https://www.two.ai/sutra/api))

## Installation 🚀

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sutra-dev/sutra-cookbook.git
   cd sutra-cookbook/starter-apps/streamlit-apps/multilingual-website-extractor
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** (optional):
   ```
   SUTRA_API_KEY=your_api_key_here
   ```

## Required Dependencies 📦

```
streamlit
beautifulsoup4
requests
python-dotenv
pandas
pydantic
langchain-openai
langdetect
```

Create a `requirements.txt` file with the above dependencies.

## Usage 💡

1. **Run the application**:
   ```bash
   streamlit run app.py
   ```

2. **Configure the app**:
   - Enter your SUTRA API key in the sidebar
   - Select your preferred output language
   - Add one or more website URLs

3. **Start chatting**:
   - Ask questions about the website content in any language
   - Get responses in your selected language
   - Use the ➕ button to add more URLs
   - Use the ➖ button to remove URLs

## How It Works 🔧

1. **Web Scraping**: The app scrapes content from provided URLs using BeautifulSoup
2. **Language Detection**: Automatically detects the language of your input
3. **Translation**: Translates questions to English for processing if needed
4. **AI Analysis**: Uses SUTRA AI model to analyze website content and answer questions
5. **Response Translation**: Translates responses back to your selected language

## Example Use Cases 📝

- **Research**: Extract information from multiple websites in your preferred language
- **Content Analysis**: Analyze website content across different languages
- **Data Extraction**: Get structured data from websites with natural language queries
- **Multilingual Support**: Help non-English speakers interact with English websites

## Tips for Best Results 💪

- **Clear Questions**: Ask specific, clear questions for better results
- **Multiple URLs**: Add multiple related URLs for comprehensive analysis
- **Language Selection**: Choose your preferred output language for consistent results
- **URL Validation**: Ensure URLs are accessible and contain relevant content

## Troubleshooting 🔧

**Common Issues:**

1. **API Key Error**: Make sure you've entered a valid SUTRA API key
2. **Website Access**: Some websites may block scraping - try different URLs
3. **Translation Issues**: The app automatically retries translation if detection fails
4. **Memory Issues**: The app includes garbage collection for better performance

## API Key Setup 🔑

1. Visit [SUTRA API](https://www.two.ai/sutra/api)
2. Sign up for a free account
3. Generate your API key
4. Enter the key in the sidebar or add it to your `.env` file

## Contributing 🤝

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License 📄

This project is open source. Please check the license file for details.

## Support 💬

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the SUTRA API documentation
3. Create an issue in the repository

---

**Made with ❤️ using Streamlit and SUTRA AI**