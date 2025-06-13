# Multilingual YouTube Chat 🎥

A powerful Streamlit application that allows you to chat with YouTube videos in multiple languages. Extract video transcripts and ask questions about video content using AI-powered natural language processing.

## Features ✨

- **YouTube Video Transcription**: Automatically transcribe any YouTube video using AssemblyAI
- **50+ Languages Support**: Chat in your preferred language including English, Hindi, Gujarati, Bengali, Tamil, Telugu, Arabic, Chinese, Japanese, and many more
- **AI-Powered Q&A**: Ask questions about video content and get intelligent responses
- **Real-time Streaming**: Get responses as they're being generated
- **Video Preview**: Watch videos directly in the app
- **Transcript Display**: View complete video transcripts
- **Smart Context**: AI answers are strictly based on video content

## Supported Languages 🗣️

The app supports 50+ languages including:
- **Indian Languages**: Hindi, Gujarati, Bengali, Tamil, Telugu, Kannada, Malayalam, Punjabi, Marathi, Urdu, Assamese, Odia, Sanskrit
- **International Languages**: English, Spanish, French, German, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, Thai, Vietnamese, and many more

## Prerequisites 📋

Before running the application, you need:

1. **Python 3.8 or higher**
2. **SUTRA API Key** - Get it free from [SUTRA API](https://www.two.ai/sutra/api)
3. **AssemblyAI API Key** - Get it from [AssemblyAI](https://www.assemblyai.com/)

## Installation 🚀

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sutra-dev/sutra-cookbook.git
   cd sutra-cookbook/starter-apps/streamlit-apps/multilingual-youtube-chat
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** (optional):
   ```
   SUTRA_API_KEY=your_sutra_api_key_here
   ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
   ```

## Required Dependencies 📦

```
streamlit
yt-dlp
requests
langchain-openai
python-dotenv
```

Create a `requirements.txt` file with the above dependencies.

## Usage 💡

1. **Run the application**:
   ```bash
   streamlit run app.py
   ```

2. **Configure API Keys**:
   - Enter your SUTRA API key in the sidebar
   - Enter your AssemblyAI API key in the sidebar

3. **Process a YouTube Video**:
   - Paste a YouTube URL in the input field
   - Select your preferred chat language
   - Click "🎬 Transcribe Video" button
   - Wait for transcription to complete

4. **Start Chatting**:
   - Ask questions about the video content
   - Get responses in your selected language
   - All answers are based strictly on the video transcript

## How It Works 🔧

1. **Video Download**: Uses `yt-dlp` to extract audio from YouTube videos
2. **Audio Upload**: Uploads audio to AssemblyAI for transcription
3. **Transcription**: AssemblyAI processes the audio and generates text transcript
4. **AI Analysis**: SUTRA AI model analyzes the transcript and answers questions
5. **Multilingual Response**: Responses are provided in your selected language

## API Keys Setup 🔑

### SUTRA API Key
1. Visit [SUTRA API](https://www.two.ai/sutra/api)
2. Sign up for a free account
3. Generate your API key
4. Enter it in the sidebar

### AssemblyAI API Key
1. Visit [AssemblyAI](https://www.assemblyai.com/)
2. Create an account
3. Get your API key from the dashboard
4. Enter it in the sidebar

## Example Use Cases 📝

- **Educational Content**: Ask questions about lectures, tutorials, or educational videos
- **Meeting Analysis**: Transcribe and analyze recorded meetings or presentations
- **Content Research**: Extract key information from long-form video content
- **Language Learning**: Practice comprehension by asking questions about foreign language videos
- **Accessibility**: Make video content accessible through text-based interaction

## Features in Detail 🔍

### Video Transcription
- High-quality audio extraction from YouTube videos
- Accurate speech-to-text conversion using AssemblyAI
- Real-time transcription status updates
- Complete transcript display

### Multilingual Chat
- Natural language processing in 50+ languages
- Context-aware responses based on video content
- Streaming responses for better user experience
- Smart error handling and validation

### User Interface
- Clean, intuitive Streamlit interface
- Expandable sections for better organization
- Video preview functionality
- Real-time status updates

## Troubleshooting 🔧

**Common Issues:**

1. **API Key Errors**:
   - Ensure both SUTRA and AssemblyAI API keys are valid
   - Check if you have sufficient API credits

2. **Video Download Issues**:
   - Some videos may be restricted or private
   - Try different YouTube URLs
   - Ensure the URL is valid and accessible

3. **Transcription Failures**:
   - Check your AssemblyAI API key
   - Ensure you have sufficient credits
   - Some videos may have poor audio quality

4. **Chat Not Working**:
   - Verify your SUTRA API key is entered correctly
   - Make sure transcription is completed before chatting

## Technical Details 🛠️

### Architecture
- **Frontend**: Streamlit web application
- **Video Processing**: yt-dlp for YouTube video extraction
- **Transcription**: AssemblyAI API for speech-to-text
- **AI Chat**: SUTRA AI model via OpenAI-compatible API
- **Streaming**: Real-time response generation with callback handlers

### Performance Optimization
- Caching for chat model initialization
- Efficient audio file handling
- Smart polling for transcription status
- Memory management for large transcripts

## Limitations ⚠️

- **YouTube Restrictions**: Some videos may not be downloadable due to copyright or privacy settings
- **Audio Quality**: Transcription accuracy depends on audio quality
- **Video Length**: Very long videos may take more time to process
- **API Limits**: Subject to API rate limits and usage quotas

## Contributing 🤝

Contributions are welcome! Please feel free to:
- Submit bug reports
- Request new features
- Create pull requests
- Improve documentation

## License 📄

This project is open source. Please check the license file for details.

## Support 💬

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify your API keys are valid
3. Review the API documentation for SUTRA and AssemblyAI
4. Create an issue in the repository

## Acknowledgments 🙏

- **SUTRA AI** for providing the multilingual chat capabilities
- **AssemblyAI** for accurate speech-to-text transcription
- **yt-dlp** for reliable YouTube video processing
- **Streamlit** for the web application framework

---

**Made with ❤️ using Streamlit, SUTRA AI, and AssemblyAI**