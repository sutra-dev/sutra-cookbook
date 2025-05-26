# 🧠 Multilingual PDF Mindmap Generator

A powerful Streamlit application that converts PDF documents into interactive, hierarchical mindmaps using AI. Supports 40+ languages and creates beautiful, navigable visualizations of your content.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🌍 **Multilingual Support**
- **40+ Languages** including English, Hindi, Arabic, Chinese, Japanese, Korean, and many more
- Native language rendering with appropriate fonts
- Language-specific mindmap generation prompts

### 📄 **PDF Processing**
- Advanced text extraction from PDF documents
- Smart text chunking for large documents
- Progress tracking during processing
- Support for multi-page documents

### 🎯 **Dual Input Methods**
- **PDF Upload**: Convert existing PDF documents
- **Topic Search**: Generate mindmaps from topic keywords

### 🎨 **Interactive Visualization**
- Beautiful, color-coded hierarchical mindmaps
- Zoom, pan, and navigation controls
- Responsive design with smooth animations
- Export-ready visualizations

### ⚙️ **Advanced Configuration**
- Customizable AI parameters (temperature, tokens, depth)
- Adjustable chunk sizes for optimal processing
- Real-time progress tracking

### 💾 **Export Options**
- Markdown (.md)
- HTML (.html) - Standalone interactive version
- Plain text (.txt)
- Statistics and metadata

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8+
pip package manager
SUTRA API key (free from https://www.two.ai/sutra/api)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/sutra-dev/sutra-cookbook.git
cd sutra-cookbook/starter-apps/mindmap-generator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables (optional)**
```bash
# Create .env file
echo "SUTRA_API_KEY=your_api_key_here" > .env
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open your browser**
Navigate to `http://localhost:8501`

## 📦 Dependencies

Create a `requirements.txt` file with:

```txt
streamlit>=1.28.0
openai>=1.0.0
PyPDF2>=3.0.0
python-dotenv>=1.0.0
asyncio
concurrent.futures
logging
dataclasses
typing
```

## 🔧 Configuration

### Environment Variables

```bash
# Optional: Set your API key in environment
SUTRA_API_KEY=your_sutra_api_key
```

### Application Settings

The application provides several configuration options:

- **Max Tokens**: 1000-8000 (default: 4000)
- **Temperature**: 0.0-1.0 (default: 0.3)
- **Chunk Size**: 4000-12000 (default: 8000)
- **Max Depth**: 2-6 levels (default: 4)

## 🎯 Usage Guide

### Method 1: PDF Upload

1. **Get API Key**: Sign up at [SUTRA API](https://www.two.ai/sutra/api)
2. **Enter API Key**: Paste your key in the sidebar
3. **Select Input Type**: Choose "PDF Upload"
4. **Upload PDF**: Click browse and select your PDF file
5. **Choose Language**: Select your preferred output language
6. **Generate**: Click to process and create your mindmap

### Method 2: Topic Search

1. **Enter API Key**: Same as above
2. **Select Input Type**: Choose "Search Topic"
3. **Enter Topic**: Type your topic (e.g., "Machine Learning", "Climate Change")
4. **Choose Language**: Select output language
5. **Generate**: Process and create mindmap

### Advanced Usage

```python
# Custom configuration example
config = MindmapConfig(
    max_tokens=6000,        # More detailed output
    temperature=0.2,        # More focused content
    chunk_size=10000,       # Larger chunks
    max_depth=5            # Deeper hierarchy
)
```

## 🌐 Supported Languages

| Region | Languages |
|--------|-----------|
| **Indian** | Hindi, Gujarati, Bengali, Tamil, Telugu, Kannada, Malayalam, Punjabi, Marathi, Urdu, Sanskrit |
| **East Asian** | Chinese, Japanese, Korean, Vietnamese, Thai |
| **European** | English, French, German, Spanish, Italian, Portuguese, Russian, Dutch, Polish, Greek, Swedish, Norwegian, Finnish |
| **Middle Eastern** | Arabic, Persian, Hebrew, Turkish |
| **Other** | Indonesian, Malay, Tagalog, Swahili, and more |

## 📊 Output Examples

### Markdown Structure
```markdown
# Main Topic
## Subtopic 1
### Detail 1.1
- Key point 1
- Key point 2
#### Sub-detail 1.1.1
### Detail 1.2
## Subtopic 2
### Detail 2.1
```

### Interactive Features
- **Zoom Controls**: In/Out/Fit to view
- **Color Coding**: Automatic depth-based coloring
- **Expandable Nodes**: Click to expand/collapse
- **Smooth Animations**: Professional transitions

## 🔒 Security & Privacy

- **API Keys**: Stored locally, never transmitted except to SUTRA API
- **Data Processing**: PDFs processed locally, only text sent to AI
- **No Storage**: No data permanently stored on servers
- **Privacy First**: Your documents remain private

## 🛠️ Technical Architecture

### Core Components

```
├── SutraClient          # AI API integration
├── PDFProcessor         # PDF text extraction
├── MindmapGenerator     # AI-powered mindmap creation
├── HTML Renderer        # Interactive visualization
└── Streamlit UI         # Web interface
```

### Processing Flow

1. **Input Processing**: PDF extraction or topic input
2. **Text Chunking**: Smart splitting for large content
3. **AI Generation**: Language-specific mindmap creation
4. **Merging**: Combining multiple chunks into coherent output
5. **Visualization**: Interactive HTML rendering with Markmap



## 📈 Performance Tips

### Optimization Strategies

1. **Chunk Size**: Larger chunks = fewer API calls but may hit limits
2. **Temperature**: Lower values (0.1-0.3) for focused content
3. **Max Tokens**: Balance between detail and processing time
4. **Concurrent Processing**: Automatic for multi-chunk documents

### Best Practices

- **PDF Quality**: Use text-based PDFs for best results
- **File Size**: Optimal size 1-20MB for good performance
- **Language Selection**: Choose based on source content language
- **Topic Specificity**: More specific topics generate better mindmaps


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SUTRA API** for powerful AI language processing
- **Markmap** for beautiful mindmap visualizations
- **Streamlit** for the amazing web framework
- **PyPDF2** for reliable PDF processing
- **Community** for language support and testing