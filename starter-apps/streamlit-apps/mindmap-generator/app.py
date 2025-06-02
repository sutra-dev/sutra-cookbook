import os
import streamlit as st
from openai import OpenAI
import PyPDF2
import streamlit.components.v1 as components
import asyncio
import concurrent.futures
from typing import Optional, List, Dict
import time
import logging
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="PDF Mindmap Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define supported languages with their native names
LANGUAGES = {
    "English": {"name": "English", "code": "en"},
    "Hindi": {"name": "हिंदी", "code": "hi"},
    "Gujarati": {"name": "ગુજરાતી", "code": "gu"},
    "Bengali": {"name": "বাংলা", "code": "bn"},
    "Tamil": {"name": "தமிழ்", "code": "ta"},
    "Telugu": {"name": "తెలుగు", "code": "te"},
    "Kannada": {"name": "ಕನ್ನಡ", "code": "kn"},
    "Malayalam": {"name": "മലയാളം", "code": "ml"},
    "Punjabi": {"name": "ਪੰਜਾਬੀ", "code": "pa"},
    "Marathi": {"name": "मराठी", "code": "mr"},
    "Urdu": {"name": "اردو", "code": "ur"},
    "Sanskrit": {"name": "संस्कृत", "code": "sa"},
    "Korean": {"name": "한국어", "code": "ko"},
    "Japanese": {"name": "日本語", "code": "ja"},
    "Arabic": {"name": "العربية", "code": "ar"},
    "French": {"name": "Français", "code": "fr"},
    "German": {"name": "Deutsch", "code": "de"},
    "Spanish": {"name": "Español", "code": "es"},
    "Portuguese": {"name": "Português", "code": "pt"},
    "Russian": {"name": "Русский", "code": "ru"},
    "Chinese": {"name": "中文", "code": "zh"},
    "Vietnamese": {"name": "Tiếng Việt", "code": "vi"},
    "Thai": {"name": "ไทย", "code": "th"},
    "Indonesian": {"name": "Bahasa Indonesia", "code": "id"},
    "Turkish": {"name": "Türkçe", "code": "tr"},
    "Italian": {"name": "Italiano", "code": "it"},
    "Dutch": {"name": "Nederlands", "code": "nl"},
    "Polish": {"name": "Polski", "code": "pl"},
    "Greek": {"name": "Ελληνικά", "code": "el"},
    "Hebrew": {"name": "עברית", "code": "he"},
    "Persian": {"name": "فارسی", "code": "fa"},
    "Swedish": {"name": "Svenska", "code": "sv"},
    "Norwegian": {"name": "Norsk", "code": "no"},
    "Finnish": {"name": "Suomi", "code": "fi"},
    "Czech": {"name": "Čeština", "code": "cs"},
    "Hungarian": {"name": "Magyar", "code": "hu"},
    "Romanian": {"name": "Română", "code": "ro"},
    "Bulgarian": {"name": "Български", "code": "bg"},
    "Croatian": {"name": "Hrvatski", "code": "hr"},
    "Serbian": {"name": "Српски", "code": "sr"},
    "Ukrainian": {"name": "Українська", "code": "uk"},
    "Malay": {"name": "Bahasa Melayu", "code": "ms"},
    "Tagalog": {"name": "Filipino", "code": "tl"},
    "Swahili": {"name": "Kiswahili", "code": "sw"}
}

@dataclass
class MindmapConfig:
    """Configuration for mindmap generation"""
    max_tokens: int = 4000
    temperature: float = 0.3
    chunk_size: int = 8000
    overlap_size: int = 200
    max_depth: int = 4

class SutraClient:
    """Enhanced Sutra API client with error handling and retry logic"""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url='https://api.two.ai/v2',
            api_key=api_key
        )
        self.api_key = api_key
    
    def generate_completion(self, messages: List[Dict], config: MindmapConfig) -> Optional[str]:
        """Generate completion with error handling and retry logic"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model='sutra-v2',
                    messages=messages,
                    max_tokens=config.max_tokens,
                    temperature=config.temperature,
                    stream=False
                )
                
                if response.choices and response.choices[0].message.content:
                    return response.choices[0].message.content.strip()
                else:
                    logger.warning(f"Empty response received on attempt {attempt + 1}")
                    
            except Exception as e:
                logger.error(f"API call failed on attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    raise e
        
        return None
    
    def generate_streaming_completion(self, messages: List[Dict], config: MindmapConfig):
        """Generate streaming completion"""
        try:
            stream = self.client.chat.completions.create(
                model='sutra-v2',
                messages=messages,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                stream=True
            )
            
            for chunk in stream:
                if len(chunk.choices) > 0:
                    content = chunk.choices[0].delta.content
                    finish_reason = chunk.choices[0].finish_reason
                    if content and finish_reason is None:
                        yield content
                        
        except Exception as e:
            logger.error(f"Streaming API call failed: {str(e)}")
            raise e

class PDFProcessor:
    """Advanced PDF processing with chunking and error handling"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_file, progress_callback=None) -> Optional[str]:
        """Extract text from PDF with progress tracking"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            total_pages = len(pdf_reader.pages)
            text_parts = []
            
            for i, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text_parts.append(page_text.strip())
                    
                    if progress_callback:
                        progress_callback((i + 1) / total_pages)
                        
                except Exception as e:
                    logger.warning(f"Error extracting text from page {i + 1}: {str(e)}")
                    continue
            
            if not text_parts:
                logger.warning("No text could be extracted from any page")
                return None
            
            full_text = "\n\n".join(text_parts)
            logger.info(f"Successfully extracted {len(full_text)} characters from {len(text_parts)} pages")
            return full_text
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            return None
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 8000, overlap_size: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            if end >= len(text):
                chunks.append(text[start:])
                break
            
            # Try to break at sentence or paragraph boundary
            chunk = text[start:end]
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            
            break_point = max(last_period, last_newline)
            if break_point > start + chunk_size * 0.7:  # If break point is reasonable
                end = start + break_point + 1
            
            chunks.append(text[start:end])
            start = end - overlap_size
        
        return chunks

class MindmapGenerator:
    """Advanced mindmap generator with multilingual support"""
    
    def __init__(self, sutra_client: SutraClient):
        self.client = sutra_client
    
    def create_mindmap_prompt(self, language: str, text: str, chunk_index: int = 0, total_chunks: int = 1) -> str:
        """Create language-specific mindmap generation prompt"""
        
        language_instructions = {
            "English": "Create a hierarchical mindmap in English",
            "Hindi": "हिंदी में एक श्रेणीबद्ध माइंडमैप बनाएं",
            "Gujarati": "ગુજરાતીમાં એક વિભાજિત માઇન્ડમેપ બનાવો",
            "Bengali": "বাংলায় একটি শ্রেণিবদ্ধ মাইণ্ডমেপ তৈরি করুন",
            "Tamil": "தமிழில் ஒரு படிநிலை மனவரைபடத்தை உருவாக்கவும்",
            "Telugu": "తెలుగులో ఒక శ్రేణీకృత మైండ్ మ్యాప్‌ని సృష్టించండి",
            "Kannada": "ಕನ್ನಡದಲ್ಲಿ ಒಂದು ಶ್ರೇಣೀಕೃತ ಮನಸ್ಸಿನ ನಕ್ಷೆಯನ್ನು ರಚಿಸಿ",
            "Malayalam": "മലയാളത്തിൽ ഒരു ശ്രേണീകൃത മൈൻഡ് മാപ്പ് സൃഷ്ടിക്കുക",
            "Punjabi": "ਪੰਜਾਬੀ ਵਿੱਚ ਇੱਕ ਲੜੀਬੱਧ ਮਾਈਂਡ ਮੈਪ ਬਣਾਓ",
            "Marathi": "मराठीमध्ये एक श्रेणीबद्ध माइंडमॅप तयार करा",
            "Assamese": "অসমীয়াত এটা শ্ৰেণীবদ্ধ মাইণ্ডমেপ সৃষ্টি কৰক",
            "Odia": "ଓଡ଼ିଆରେ ଏକ ଶ୍ରେଣୀବଦ୍ଧ ମାଇଣ୍ଡମ୍ୟାପ୍ ସୃଷ୍ଟି କରନ୍ତୁ",
            "Sanskrit": "संस्कृतभाषायां श्रेणीबद्धं मनःमानचित्रं निर्माणं कुरुत",
            "French": "Créez une carte mentale hiérarchique en français",
            "German": "Erstellen Sie eine hierarchische Mindmap auf Deutsch",
            "Spanish": "Crea un mapa mental jerárquico en español",
            "Portuguese": "Crie um mapa mental hierárquico em português",
            "Russian": "Создайте иерархическую карту мыслей на русском языке",
            "Chinese": "用中文创建一个分层思维导图",
            "Vietnamese": "Tạo một sơ đồ tư duy phân cấp bằng tiếng Việt",
            "Thai": "สร้างแผนที่ความคิดแบบลำดับชั้นเป็นภาษาไทย",
            "Indonesian": "Buat peta pikiran hierarkis dalam bahasa Indonesia",
            "Turkish": "Türkçe'de hiyerarşik bir zihin haritası oluşturun",
            "Polish": "Utwórz hierarchiczną mapę myśli po polsku",
            "Ukrainian": "Створіть ієрархічну карту думок українською мовою",
            "Dutch": "Maak een hiërarchische mindmap in het Nederlands",
            "Italian": "Crea una mappa mentale gerarchica in italiano",
            "Greek": "Δημιουργήστε ένα ιεραρχικό χάρτη σκέψης στα ελληνικά",
            "Swedish": "Skapa en hierarkisk tankekarta på svenska",
            "Norwegian": "Lag et hierarkisk tankekart på norsk",
            "Danish": "Opret et hierarkisk tankekort på dansk",
            "Finnish": "Luo hierarkkinen ajatuskartta suomeksi",
            "Czech": "Vytvořte hierarchickou myšlenkovou mapu v češtině",
            "Hungarian": "Készítsen hierarchikus gondolatképet magyarul",
            "Romanian": "Creați o hartă mentală ierarhică în limba română",
            "Bulgarian": "Създайте йерархична мисловна карта на български",
            "Croatian": "Stvorite hijerarhijsku mapu uma na hrvatskom jeziku",
            "Serbian": "Направите хијерархијску мапу ума на српском језику",
            "Slovak": "Vytvorte hierarchickú myšlienkovú mapu v slovenčine",
            "Slovenian": "Ustvarite hierarhično miselno karto v slovenščini",
            "Estonian": "Looge hierarhiline mõttekaart eesti keeles",
            "Latvian": "Izveidojiet hierarhisku prāta karti latviešu valodā",
            "Lithuanian": "Sukurkite hierarchinę minties žemėlapį lietuvių kalba",
            "Malay": "Buat peta minda hierarki dalam bahasa Melayu",
            "Tagalog": "Gumawa ng hierarchical mind map sa Tagalog",
            "Swahili": "Unda ramani ya akili ya kihierarkia kwa Kiswahili"
        }
        
        instruction = language_instructions.get(language, f"Create a hierarchical mindmap in {language}")
        
        base_prompt = f"""
{instruction} from the following text content.

IMPORTANT FORMATTING RULES:
- Use proper markdown heading syntax (# for main topics, ## for subtopics, ### for details, #### for sub-details)
- Focus on the main concepts, key ideas, and their relationships
- Include relevant details and connections between ideas
- Keep the structure clean, organized, and logical
- Use bullet points (-) for listing key points under each heading
- Ensure the mindmap flows naturally from general to specific concepts
- Maximum depth of 4 levels (# to ####)

FORMAT EXAMPLE:
# Main Topic 1
## Subtopic 1.1
### Detail 1.1.1
- Key point 1
- Key point 2
#### Sub-detail 1.1.1.1
### Detail 1.1.2
- Key point 1
## Subtopic 1.2

# Main Topic 2
## Subtopic 2.1
### Detail 2.1.1

Text to analyze: {text}

Respond ONLY with the markdown mindmap structure in {language}, no additional explanations or text.
"""
        
        if total_chunks > 1:
            base_prompt += f"\n\nNote: This is chunk {chunk_index + 1} of {total_chunks}. Focus on the main concepts in this section."
        
        return base_prompt
    
    def generate_mindmap_for_chunk(self, text: str, language: str, chunk_index: int, total_chunks: int, config: MindmapConfig) -> Optional[str]:
        """Generate mindmap for a single text chunk"""
        prompt = self.create_mindmap_prompt(language, text, chunk_index, total_chunks)
        
        messages = [
            {"role": "system", "content": f"You are an expert in creating structured mindmaps in {language}. Create clear, hierarchical mindmaps using proper markdown formatting."},
            {"role": "user", "content": prompt}
        ]
        
        return self.client.generate_completion(messages, config)
    
    def merge_mindmaps(self, mindmaps: List[str], language: str, config: MindmapConfig) -> Optional[str]:
        """Merge multiple mindmaps into a single coherent mindmap"""
        if len(mindmaps) == 1:
            return mindmaps[0]
        
        combined_content = "\n\n".join([f"SECTION {i+1}:\n{mindmap}" for i, mindmap in enumerate(mindmaps)])
        
        merge_prompt = f"""
Merge the following mindmap sections into a single, coherent, hierarchical mindmap in {language}.

MERGING RULES:
1. Combine similar topics and subtopics
2. Eliminate redundancy while preserving important details
3. Maintain logical hierarchy (# to #### levels)
4. Ensure smooth flow between concepts
5. Keep the structure clean and organized
6. Use proper markdown formatting

CONTENT TO MERGE:
{combined_content}

Create a unified mindmap in {language} that encompasses all the key concepts from the sections above.
Respond ONLY with the final merged markdown mindmap.
"""
        
        messages = [
            {"role": "system", "content": f"You are an expert in consolidating and organizing information into coherent mindmaps in {language}."},
            {"role": "user", "content": merge_prompt}
        ]
        
        return self.client.generate_completion(messages, config)
    
    async def generate_mindmap(self, text: str, language: str, config: MindmapConfig, progress_callback=None) -> Optional[str]:
        """Generate mindmap with chunking support"""
        try:
            # Split text into chunks if necessary
            chunks = PDFProcessor.chunk_text(text, config.chunk_size)
            
            if len(chunks) == 1:
                # Single chunk processing
                if progress_callback:
                    progress_callback(0.5, "Generating mindmap...")
                
                result = self.generate_mindmap_for_chunk(chunks[0], language, 0, 1, config)
                
                if progress_callback:
                    progress_callback(1.0, "Mindmap generated successfully!")
                
                return result
            
            else:
                # Multi-chunk processing
                mindmaps = []
                
                # Process chunks concurrently
                with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                    futures = []
                    
                    for i, chunk in enumerate(chunks):
                        future = executor.submit(
                            self.generate_mindmap_for_chunk,
                            chunk, language, i, len(chunks), config
                        )
                        futures.append(future)
                    
                    for i, future in enumerate(concurrent.futures.as_completed(futures)):
                        try:
                            result = future.result()
                            if result:
                                mindmaps.append(result)
                            
                            if progress_callback:
                                progress = (i + 1) / len(chunks) * 0.8
                                progress_callback(progress, f"Processing chunk {i + 1}/{len(chunks)}...")
                                
                        except Exception as e:
                            logger.error(f"Error processing chunk: {str(e)}")
                
                if not mindmaps:
                    return None
                
                # Merge mindmaps
                if progress_callback:
                    progress_callback(0.9, "Merging mindmap sections...")
                
                final_mindmap = self.merge_mindmaps(mindmaps, language, config)
                
                if progress_callback:
                    progress_callback(1.0, "Mindmap generated successfully!")
                
                return final_mindmap
                
        except Exception as e:
            logger.error(f"Error generating mindmap: {str(e)}")
            return None

def create_enhanced_markmap_html(markdown_content: str, language: str) -> str:
    """Create enhanced HTML with Markmap visualization and language-specific styling"""
    
    # Escape content for JavaScript
    escaped_content = markdown_content.replace('`', '\\`').replace('${', '\\${').replace('\\', '\\\\')
    
    # Language-specific styling
    font_family = "Arial, sans-serif"
    if language in ["Hindi", "Sanskrit", "Marathi", "Gujarati"]:
        font_family = "Noto Sans Devanagari, Arial, sans-serif"
    elif language in ["Arabic", "Persian", "Urdu"]:
        font_family = "Noto Sans Arabic, Arial, sans-serif"
    elif language in ["Chinese"]:
        font_family = "Noto Sans CJK SC, Arial, sans-serif"
    elif language in ["Japanese"]:
        font_family = "Noto Sans CJK JP, Arial, sans-serif"
    elif language in ["Korean"]:
        font_family = "Noto Sans CJK KR, Arial, sans-serif"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Interactive Mindmap</title>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600&family=Noto+Sans+Devanagari:wght@400;600&family=Noto+Sans+Arabic:wght@400;600&family=Noto+Sans+CJK+SC:wght@400;600&family=Noto+Sans+CJK+JP:wght@400;600&family=Noto+Sans+CJK+KR:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: {font_family};
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                overflow: hidden;
            }}
            #mindmap {{
                width: 100vw;
                height: 100vh;
                display: block;
            }}
            .mm-node text {{
                font-family: {font_family};
                font-weight: 500;
            }}
            .loading {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: white;
                font-size: 18px;
                z-index: 1000;
            }}
            .controls {{
                position: absolute;
                top: 20px;
                right: 20px;
                z-index: 1000;
                background: rgba(255, 255, 255, 0.9);
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }}
            .control-btn {{
                background: #4CAF50;
                color: white;
                border: none;
                padding: 8px 12px;
                margin: 2px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 12px;
            }}
            .control-btn:hover {{
                background: #45a049;
            }}
            .language-info {{
                position: absolute;
                bottom: 20px;
                left: 20px;
                background: rgba(255, 255, 255, 0.9);
                padding: 10px 15px;
                border-radius: 8px;
                font-size: 14px;
                color: #333;
                z-index: 1000;
            }}
        </style>
        <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view@0.15.3/dist/browser/index.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-lib@0.15.3/dist/browser/index.min.js"></script>
    </head>
    <body>
        <div class="loading" id="loading">Loading mindmap...</div>
        <div class="controls" id="controls" style="display: none;">
            <button class="control-btn" onclick="zoomIn()">Zoom In</button>
            <button class="control-btn" onclick="zoomOut()">Zoom Out</button>
            <button class="control-btn" onclick="fitView()">Fit View</button>
        </div>
        <div class="language-info">
            <strong>Language:</strong> {language}
        </div>
        <svg id="mindmap"></svg>
        
        <script>
            let mm;
            
            window.onload = async () => {{
                try {{
                    const markdown = `{escaped_content}`;
                    
                    if (!markdown.trim()) {{
                        throw new Error('No mindmap content provided');
                    }}
                    
                    const {{ Transformer }} = markmap;
                    const transformer = new Transformer();
                    const {{root, features}} = transformer.transform(markdown);
                    
                    const {{ Markmap, loadCSS, loadJS }} = markmap;
                    
                    // Load required assets
                    if (features.styles) loadCSS(features.styles);
                    if (features.scripts) await loadJS(features.scripts);
                    
                    const svgElement = document.querySelector('#mindmap');
                    mm = new Markmap(svgElement, {{
                        color: (node) => {{
                            const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'];
                            return colors[node.depth % colors.length];
                        }},
                        duration: 800,
                        maxWidth: 300,
                        paddingX: 12,
                        paddingY: 8,
                        spacingVertical: 10,
                        spacingHorizontal: 80,
                        autoFit: true,
                        pan: true,
                        zoom: true,
                        initialExpandLevel: 2,
                        embedGlobalCSS: false
                    }});
                    
                    mm.setData(root);
                    mm.fit();
                    
                    // Hide loading and show controls
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('controls').style.display = 'block';
                    
                }} catch (error) {{
                    console.error('Error rendering mindmap:', error);
                    document.getElementById('loading').innerHTML = 
                        '<div style="color: #ff6b6b;">Error loading mindmap: ' + error.message + '</div>';
                }}
            }};
            
            function zoomIn() {{
                if (mm) mm.rescale(1.2);
            }}
            
            function zoomOut() {{
                if (mm) mm.rescale(0.8);
            }}
            
            function fitView() {{
                if (mm) mm.fit();
            }}
        </script>
    </body>
    </html>
    """
    
    return html_content

def main():
    """Main application function"""
    
    # Custom CSS
    st.markdown("""
    <style>
    .stProgress .st-bo {
        background-color: #667eea;
    }
    .search-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown(
        f'<h1><img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png" width="60" style="vertical-align: middle;"/>  Multilingual Mindmap Generator</h1>',
        unsafe_allow_html=True
    )
    
    # Sidebar configuration
    with st.sidebar:
        st.title("Configuration")
        
        # API Key input
        st.markdown("**SUTRA API**")
        st.markdown("Get your free API key from [SUTRA API](https://www.two.ai/sutra/api)")
        api_key = st.text_input("Enter your SUTRA API Key:", 
                               value=st.session_state.get('sutra_api_key', ''),
                               type="password",
                               label_visibility="collapsed")
        
        if not api_key:
            st.warning("Please enter your API key to continue")
            return

        # Input Type Selection
        st.markdown("### Input Type")
        input_type = st.radio(
            "Choose input type:",
            ["PDF Upload", "Search Topic"],
            key="input_type"
        )

        if input_type == "PDF Upload":
            # Upload PDF Document
            st.markdown("### Upload PDF Document")
            uploaded_file = st.file_uploader(
                "Choose a PDF file to convert to mindmap",
                type="pdf"
            )
            search_topic = None
        else:
            # Search Option
            st.markdown("### Search Topic")
            search_topic = st.text_input(
                "Enter a topic to generate mindmap",
                placeholder="e.g., Artificial Intelligence, Climate Change, etc."
            )
            uploaded_file = None
        
        # Language selection
        st.markdown("### Language Selection")
        selected_language = st.selectbox(
            "Choose output language:",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: f"{LANGUAGES[x]['name']} ({x})",
            key="language"
        )
        
        # Advanced settings
        st.markdown("### Advanced Settings")
        
        with st.expander("Mindmap Configuration"):
            max_tokens = st.slider("Max Tokens", 1000, 8000, 4000, 500)
            temperature = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.3, 0.1)
            chunk_size = st.slider("Chunk Size", 4000, 12000, 8000, 1000)
            max_depth = st.slider("Max Depth Levels", 2, 6, 4, 1)
        
        config = MindmapConfig(
            max_tokens=max_tokens,
            temperature=temperature,
            chunk_size=chunk_size,
            max_depth=max_depth
        )
    
    # Initialize clients
    sutra_client = SutraClient(api_key)
    mindmap_generator = MindmapGenerator(sutra_client)

    # Process based on input type
    if (input_type == "PDF Upload" and uploaded_file is not None) or (input_type == "Search Topic" and search_topic):
        try:
            # Create progress containers
            progress_container = st.container()
            
            with progress_container:
                st.markdown("### Processing Status")
                progress_bar = st.progress(0)
                status_text = st.empty()

                if input_type == "PDF Upload":
                    # Extract text from PDF
                    status_text.text("Extracting text from PDF...")
                    
                    def update_pdf_progress(progress):
                        progress_bar.progress(progress * 0.3)
                        status_text.text(f"Extracting text... {int(progress * 100)}%")
                    
                    extracted_text = PDFProcessor.extract_text_from_pdf(uploaded_file, update_pdf_progress)
                    
                    if not extracted_text:
                        st.error("Could not extract text from the PDF. Please ensure it's not a scanned document.")
                        return
                    
                    # Display text statistics
                    text_stats = {
                        "characters": len(extracted_text),
                        "words": len(extracted_text.split()),
                        "chunks": len(PDFProcessor.chunk_text(extracted_text, config.chunk_size))
                    }
                    
                    st.info(f"Successfully extracted {text_stats['characters']:,} characters, {text_stats['words']:,} words in {text_stats['chunks']} chunks")
                    input_text = extracted_text
                else:
                    # Use search topic
                    status_text.text("Generating content from search topic...")
                    input_text = search_topic
                    text_stats = {
                        "characters": len(search_topic),
                        "words": len(search_topic.split()),
                        "chunks": 1
                    }
                
                # Generate mindmap
                status_text.text("Generating mindmap...")
                
                def update_mindmap_progress(progress, message):
                    total_progress = 0.3 + (progress * 0.7)
                    progress_bar.progress(total_progress)
                    status_text.text(message)
                
                # Use asyncio to handle async mindmap generation
                import asyncio
                
                async def generate_mindmap_async():
                    return await mindmap_generator.generate_mindmap(
                        input_text, 
                        selected_language, 
                        config, 
                        update_mindmap_progress
                    )
                
                # Run the async function
                try:
                    mindmap_content = asyncio.run(generate_mindmap_async())
                except RuntimeError:
                    import threading
                    result = [None]
                    exception = [None]
                    
                    def run_in_thread():
                        try:
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            result[0] = loop.run_until_complete(generate_mindmap_async())
                        except Exception as e:
                            exception[0] = e
                        finally:
                            loop.close()
                    
                    thread = threading.Thread(target=run_in_thread)
                    thread.start()
                    thread.join()
                    
                    if exception[0]:
                        raise exception[0]
                    mindmap_content = result[0]
                
                progress_bar.progress(1.0)
                status_text.text("Mindmap generated successfully!")
                
                if not mindmap_content:
                    st.error("Failed to generate mindmap. Please try again.")
                    return
            
            # Display results in tabs
            st.markdown("---")
            st.markdown("### Generated Mindmap")
            
            tab_mindmap, tab_markdown, tab_export = st.tabs([
                "Interactive Mindmap", 
                "Markdown Source", 
                "Export Options"
            ])
            
            with tab_mindmap:
                st.markdown("#### Interactive Visualization")
                st.markdown(f"**Language:** {LANGUAGES[selected_language]['name']} ({selected_language})")
                
                # Create and display the interactive mindmap
                html_content = create_enhanced_markmap_html(mindmap_content, selected_language)
                components.html(html_content, height=700, scrolling=False)
                
                # Mindmap statistics
                lines = mindmap_content.split('\n')
                main_topics = len([line for line in lines if line.startswith('# ')])
                subtopics = len([line for line in lines if line.startswith('## ')])
                details = len([line for line in lines if line.startswith('### ')])
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Main Topics", main_topics)
                with col2:
                    st.metric("Subtopics", subtopics)
                with col3:
                    st.metric("Details", details)
                with col4:
                    st.metric("Total Lines", len(lines))
            
            with tab_markdown:
                st.markdown("#### Markdown Source Code")
                st.code(mindmap_content, language="markdown")
            
            with tab_export:
                st.markdown("#### Export Options")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Download Formats:**")
                    
                    # Download markdown
                    st.download_button(
                        label="Download Markdown (.md)",
                        data=mindmap_content,
                        file_name=f"mindmap_{selected_language.lower()}_{int(time.time())}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                    
                    # Download HTML
                    html_standalone = create_enhanced_markmap_html(mindmap_content, selected_language)
                    st.download_button(
                        label="Download HTML (.html)",
                        data=html_standalone,
                        file_name=f"mindmap_{selected_language.lower()}_{int(time.time())}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                    
                    # Download as text
                    st.download_button(
                        label="Download Text (.txt)",
                        data=mindmap_content,
                        file_name=f"mindmap_{selected_language.lower()}_{int(time.time())}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    st.markdown("**Export Statistics:**")
                    st.json({
                        "language": selected_language,
                        "total_characters": len(mindmap_content),
                        "total_lines": len(mindmap_content.split('\n')),
                        "main_topics": len([line for line in mindmap_content.split('\n') if line.startswith('# ')]),
                        "processing_time": "Real-time",
                        "chunks_processed": text_stats["chunks"],
                        "source_words": text_stats["words"]
                    })
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logger.error(f"Application error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()