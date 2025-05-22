# 📚 SUTRA Document Chatbot - Multilingual RAG Application

A Streamlit application that allows users to  chat with their documents in 34+ languages using the Sutra LLM and RAG (Retrieval-Augmented Generation) technology.

## 🌟 Features

- **Document Processing**: Upload and process PDF and DOCX files for interactive querying
- **Retrieval-Augmented Generation**: Uses RAG technology to provide context-aware responses from your documents
- **Extensive Language Support**: Generate responses in 34+ languages including English, Hindi, Gujarati, Bengali, Tamil, and many international languages
- **Real-time Streaming**: Experience fluid conversations with streaming responses
- **Interactive Chat Interface**: User-friendly chat UI for intuitive document querying
- **Vector Search**: Advanced embedding-based search to find relevant document sections
- **Context-Aware Responses**: Answers are grounded in the content of your documents
- **Responsive Design**: Works well on both desktop and mobile devices
- **Session Management**: Maintains conversation history within your session

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Sutra API Key (from Two.ai)
- OpenAI API Key (for embeddings)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/sutra-dev/sutra-cookbook.git
   cd Sutra_Cookbooks/starter-apps/Document_RAG_ChatBOT
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API keys:
   - Create a `.env` file with your API keys:
     ```
     SUTRA_API_KEY=your_sutra_api_key_here
     OPENAI_API_KEY=your_openai_api_key_here
     ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## 💡 How to Use

1. Launch the application using the command above
2. From the sidebar, select your preferred language for responses
3. Upload one or more PDF or DOCX files using the file uploader
4. Click "Process Documents" to prepare them for querying
5. Once processing is complete, use the chat input at the bottom to ask questions about your documents
6. Receive context-aware responses in your chosen language
7. Continue the conversation with follow-up questions

## 📋 Document Processing

The application processes your documents in several steps:

1. **Document Loading**: Converts PDFs and DOCX files into processable text
2. **Text Chunking**: Splits documents into manageable chunks with appropriate overlap
3. **Embedding Generation**: Creates vector representations of document chunks
4. **Vector Indexing**: Builds a searchable index using FAISS technology
5. **RAG Integration**: Sets up a conversational retrieval chain for contextual responses

## 🌍 Supported Languages

The application supports 34+ languages including:
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
- Sanskrit (संस्कृत)
- Korean (한국어)
- Japanese (日本語)
- And many more international languages

## 🎨 Technical Details

This application uses:
- **Streamlit** for the interactive web interface
- **LangChain** for document processing and RAG implementation
- **Sutra LLM API** for multilingual response generation
- **OpenAI Embeddings** for vector representation of text
- **FAISS** for efficient similarity search and retrieval
- **RecursiveCharacterTextSplitter** for intelligent document chunking
- **ConversationalRetrievalChain** for maintaining context across interactions
- **StreamHandler** for real-time response streaming
- **Environment variables** for secure API key management

## 🔒 Privacy & Security

- Documents are processed locally within your session
- No document content is stored permanently
- API keys are securely managed using environment variables
- Temporary files are cleaned up after processing
- All conversations remain within your browser session

## 🎯 Target Users

- **Researchers** working with multiple academic papers
- **Legal professionals** analyzing case documents
- **Students** studying textbooks and course materials
- **Business analysts** reviewing reports and documentation
- **Content creators** referencing source materials
- **Customer support** accessing product documentation
- **Multilingual users** needing responses in their preferred language

## 🌱 Key Benefits

- **Time Efficiency**: Quickly extract information from lengthy documents
- **Language Accessibility**: Interact with documents in your preferred language
- **Contextual Understanding**: Get answers specifically related to your content
- **Research Enhancement**: Accelerate the analysis of multiple documents
- **Knowledge Discovery**: Identify connections across different texts
- **Learning Aid**: Improve comprehension of complex materials
- **Reduced Cognitive Load**: Let the AI find relevant information for you

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Sutra LLM](https://www.two.ai/sutra) for the powerful multilingual language model
- [OpenAI](https://openai.com/) for embedding technology
- [LangChain](https://www.langchain.com) for the RAG framework
- [FAISS](https://github.com/facebookresearch/faiss) for vector search capabilities
- [Streamlit](https://streamlit.io) for the web application framework
- [Python-dotenv](https://github.com/theskumar/python-dotenv) for environment variable management
