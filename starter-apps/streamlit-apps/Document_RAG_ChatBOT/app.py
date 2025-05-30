import os
import tempfile
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.callbacks.base import BaseCallbackHandler
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("SUTRA_API_KEY")
embedding_api_key = os.getenv("OPENAI_API_KEY")  

# Page configuration
st.set_page_config(
    page_title="Sutra RAG Chat",
    page_icon="📚",
    layout="wide"
)

# Define supported languages
languages = [
    "English", "Hindi", "Gujarati", "Bengali", "Tamil", 
    "Telugu", "Kannada", "Malayalam", "Punjabi", "Marathi", 
    "Urdu", "Assamese", "Odia", "Sanskrit", "Korean", 
    "Japanese", "Arabic", "French", "German", "Spanish", 
    "Portuguese", "Russian", "Chinese", "Vietnamese", "Thai", 
    "Indonesian", "Turkish", "Polish", "Ukrainian", "Dutch", 
    "Italian", "Greek", "Hebrew", "Persian"
]

# Streaming callback handler
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None
    
    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

# Create a streaming version of the model with callback handler
def get_streaming_chat_model(callback_handler=None):
    return ChatOpenAI(
        api_key=os.getenv("SUTRA_API_KEY"),
        base_url="https://api.two.ai/v2",
        model="sutra-v2",
        temperature=0.7,
        streaming=True,
        callbacks=[callback_handler] if callback_handler else None
    )

# Get regular chat model for RAG
def get_chat_model():
    return ChatOpenAI(
        api_key=os.getenv("SUTRA_API_KEY"),
        base_url="https://api.two.ai/v2",
        model="sutra-v2",
        temperature=0.7
    )

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False

# Function to process documents
def process_documents(uploaded_files, chunk_size=1000, chunk_overlap=100):
    documents = []
    temp_dir = tempfile.TemporaryDirectory()
    
    for file in uploaded_files:
        # Save the uploaded file to a temporary file
        temp_path = os.path.join(temp_dir.name, file.name)
        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())
        
        # Process based on file type
        if file.name.endswith(".pdf"):
            loader = PyPDFLoader(temp_path)
            documents.extend(loader.load())
        elif file.name.endswith(".docx"):
            loader = Docx2txtLoader(temp_path)
            documents.extend(loader.load())
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    document_chunks = text_splitter.split_documents(documents)
    
    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings(api_key=embedding_api_key)
    vectorstore = FAISS.from_documents(document_chunks, embeddings)
    
    # Create conversation chain
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=get_chat_model(),
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    
    return conversation_chain

# App title
st.markdown(
    f'<h1><img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png" width="60"/> Sutra Document Chatbot 📚</h1>',
    unsafe_allow_html=True
    )

# Sidebar
st.sidebar.image("https://framerusercontent.com/images/3Ca34Pogzn9I3a7uTsNSlfs9Bdk.png", use_container_width=True)
with st.sidebar:
    st.title("Settings")
    
    # Language selector
    selected_language = st.selectbox("Select language for responses:", languages)
    
    # Document uploader
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF or DOCX files", 
        type=["pdf", "docx"], 
        accept_multiple_files=True
    )
    
    # Process documents button
    if uploaded_files:
        if st.button("Process Documents"):
            with st.spinner("Processing documents..."):
                # Process documents and create conversation chain
                st.session_state.conversation = process_documents(uploaded_files)
                st.session_state.documents_processed = True
                st.success(f"{len(uploaded_files)} documents processed!")
    
    st.divider()
    st.markdown(f"Responses will be in: **{selected_language}**")

# Main chat area
if not st.session_state.documents_processed:
    st.info("Please upload documents and click 'Process Documents' in the sidebar to start chatting.")
else:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask a question about your documents...")
    
    # Process user input
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Generate response
        try:
            # Create message placeholder
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                
                # Create a stream handler for real-time response
                stream_handler = StreamHandler(response_placeholder)
                
                # Get streaming model with handler
                chat = get_streaming_chat_model(stream_handler)
                
                # Get RAG context first
                rag_response = st.session_state.conversation.invoke(user_input)
                context = rag_response["answer"]
                
                # Now generate a response with Sutra in the selected language
                system_message = f"""
                You are a helpful assistant that answers questions about documents. 
                Use the following context to answer the question.
                
                CONTEXT:
                {context}
                
                Please respond in {selected_language}.
                """
                
                messages = [
                    HumanMessage(content=f"{system_message}\n\nQuestion: {user_input}")
                ]
                
                response = chat.invoke(messages)
                answer = response.content
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            if "API key" in str(e):
                st.error("Please check your API keys in the environment variables.")
