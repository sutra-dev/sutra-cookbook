# Retrieval-Augmented Generation (RAG) with SUTRA

This directory contains examples and best practices for implementing Retrieval-Augmented Generation (RAG) systems using SUTRA. Learn how to build powerful question-answering systems over your own documents and data.

## Included Notebooks

### Basic RAG Implementations
- [Chat with PDF using Pinecone](chat_with_pdf_using_pinecone.ipynb) ([Open in Colab](https://colab.research.google.com/github/Shubhwithai/sutra-cookbook/blob/main/chat-with-data/chat_with_pdf_using_pinecone.ipynb)) - Build a PDF chatbot using SUTRA and Pinecone vector database
- [Multilingual Chat with PDF](multilingual_chat_with_pdf.ipynb) ([Open in Colab](https://colab.research.google.com/github/Shubhwithai/sutra-cookbook/blob/main/chat-with-data/multilingual_chat_with_pdf.ipynb)) - Create a PDF chatbot that works in multiple languages
- [Multilingual Chat with URL](multilingual_chat_with_url.ipynb) ([Open in Colab](https://colab.research.google.com/github/Shubhwithai/sutra-cookbook/blob/main/chat-with-data/multilingual_chat_with_url.ipynb)) - Build a chatbot that can process content from web URLs in multiple languages

### Advanced RAG Techniques
- [Contextual RAG using SUTRA](contextual_rag_using_sutra.ipynb) ([Open in Colab](https://colab.research.google.com/github/Shubhwithai/sutra-cookbook/blob/main/chat-with-data/contextual_rag_using_sutra.ipynb)) - Implement contextual compression to improve retrieval relevance and efficiency
- [Hybrid RAG using SUTRA](hybrid_rag_using_sutra.ipynb) ([Open in Colab](https://colab.research.google.com/github/Shubhwithai/sutra-cookbook/blob/main/chat-with-data/hybrid_rag_using_sutra.ipynb)) - Combine vector similarity search with traditional search methods like BM25
- [HyDE RAG using SUTRA](hyde_rag_using_sutra.ipynb) ([Open in Colab](https://colab.research.google.com/github/Shubhwithai/sutra-cookbook/blob/main/chat-with-data/hyde_rag_using_sutra.ipynb)) - Implement Hypothetical Document Embeddings to improve retrieval quality
- [RAG Fusion using SUTRA](rag_fusion_using_sutra.ipynb) ([Open in Colab](https://colab.research.google.com/github/Shubhwithai/sutra-cookbook/blob/main/chat-with-data/rag_fusion_using_sutra.ipynb)) - Use query generation and Reciprocal Rank Fusion for better document retrieval

## Contents

- RAG architecture patterns
- Vector database integrations
- Document processing pipelines
- Query optimization techniques
- Advanced retrieval strategies
- Evaluation frameworks

## Key Concepts

- Document chunking and embedding
- Semantic search implementation
- Context augmentation strategies
- Hybrid retrieval approaches
- Query reformulation techniques
- Reciprocal Rank Fusion
- Contextual compression
- Hypothetical Document Embeddings

## Use Cases

- Question answering over private data
- Knowledge base assistants
- Document summarization
- Factual grounding for LLM outputs
- Multilingual information retrieval
- Web content analysis

## Prerequisites

- Basic Python programming knowledge
- Familiarity with Jupyter or Google Colab (recommended)
- [Get your SUTRA API key](https://www.two.ai/sutra/api) (free for signup)
- Access to vector databases (Pinecone offers a free tier)

## How to Use

1. **Open any notebook above in Google Colab** (recommended) or your local Jupyter environment.
2. **Install dependencies** (see the first cell in each notebook).
3. **Add your SUTRA API key** and vector database credentials when prompted.
4. **Upload your PDF documents** or provide URLs to test the RAG implementation.
5. **Run the cells and experiment!**
