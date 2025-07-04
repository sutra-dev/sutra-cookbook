from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import requests
import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Global News Hub API",
    description="API for fetching and translating global news in 50+ languages",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this based on your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class NewsItem(BaseModel):
    title: str
    snippet: str
    source: str
    link: str
    date: Optional[str] = None
    imageUrl: Optional[str] = None

class TranslateRequest(BaseModel):
    news_items: List[Dict[str, Any]]
    target_language: str
    sutra_api_key: str

class SearchRequest(BaseModel):
    query: str
    num_results: int = Field(default=10, ge=5, le=30)
    language: Optional[str] = None
    page: int = Field(default=1, ge=1)
    serper_api_key: str
    translate_to: Optional[str] = None
    sutra_api_key: Optional[str] = None

class TranslateQueryRequest(BaseModel):
    query: str
    sutra_api_key: str

# Supported languages
SUPPORTED_LANGUAGES = [
    "English", "Hindi", "Gujarati", "Bengali", "Tamil", 
    "Telugu", "Kannada", "Malayalam", "Punjabi", "Marathi", 
    "Urdu", "Assamese", "Odia", "Sanskrit", "Korean", 
    "Japanese", "Arabic", "French", "German", "Spanish", 
    "Portuguese", "Russian", "Chinese", "Vietnamese", "Thai", 
    "Indonesian", "Turkish", "Polish", "Ukrainian", "Dutch", 
    "Italian", "Greek", "Hebrew", "Persian", "Swedish", 
    "Norwegian", "Danish", "Finnish", "Czech", "Hungarian", 
    "Romanian", "Bulgarian", "Croatian", "Serbian", "Slovak", 
    "Slovenian", "Estonian", "Latvian", "Lithuanian", "Malay", 
    "Tagalog", "Swahili"
]

# Helper functions
def get_chat_model(api_key: str):
    """Initialize the ChatOpenAI model"""
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://api.two.ai/v2",
        model="sutra-v2",
        temperature=0.3,
    )

def fetch_high_quality_image(query: str, serper_api_key: str) -> Optional[str]:
    """Fetch high-quality image using Serper Images API"""
    url = "https://google.serper.dev/images"
    payload = json.dumps({
        "q": query,
        "num": 1
    })
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        results = response.json()
        if results.get("images") and len(results["images"]) > 0:
            return results["images"][0].get("imageUrl")
        return None
    except Exception as e:
        print(f"Error fetching high-quality image: {str(e)}")
        return None

def fetch_news(query: str, num_results: int, serper_api_key: str, 
               language: Optional[str] = None, page: int = 1) -> List[Dict[str, Any]]:
    """Fetch news using Serper API"""
    url = "https://google.serper.dev/news"
    payload = {
        "q": query,
        "num": num_results
    }
    
    if language:
        payload["hl"] = language.lower()
    if page > 1:
        payload["page"] = page
        
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        results = response.json()
        news_items = results.get("news", [])
        
        # Enhance news items with high-quality images
        enhanced_news_items = []
        for item in news_items:
            high_quality_image = fetch_high_quality_image(item.get('title', ''), serper_api_key)
            if high_quality_image:
                item['imageUrl'] = high_quality_image
            enhanced_news_items.append(item)
        
        return enhanced_news_items
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

def translate_news_item(item: Dict[str, Any], target_language: str, model: ChatOpenAI) -> Dict[str, Any]:
    """Translate a single news item"""
    system_message = f"""
    You are a professional translator specializing in news translation. Translate the following news content to {target_language}.
    
    Translation Rules:
    1. Translate ONLY these fields:
       - title: Keep it concise and engaging
       - snippet: Maintain the news context and tone
       - source: Translate the source name if it has a common translation
    
    2. Translation Guidelines:
       - Ensure natural and fluent language
       - Maintain the original meaning and context
       - Keep any proper nouns (names, places) in their original form
       - Preserve any numbers, dates, and measurements
       - Keep any technical terms accurate
    
    3. Return ONLY the translated fields in this exact format:
    {{
        "title": "translated title",
        "snippet": "translated snippet",
        "source": "translated source"
    }}
    
    4. Important:
       - Do not add any explanations
       - Do not modify the JSON structure
       - Do not translate any other fields
       - Ensure the translation is culturally appropriate for {target_language} speakers
    """
    
    fields_to_translate = {
        "title": item.get('title', ''),
        "snippet": item.get('snippet', ''),
        "source": item.get('source', '')
    }
    
    item_json = json.dumps(fields_to_translate, ensure_ascii=False)
    
    messages = [
        HumanMessage(content=f"{system_message}\n\nFields to translate:\n{item_json}")
    ]
    
    try:
        response = model.invoke(messages)
        result = response.content.strip()
        result = result.replace('```json', '').replace('```', '').strip()
        
        translated_fields = json.loads(result)
        
        # Create new item with translated fields and original data
        translated_item = {
            **item,
            "title": translated_fields.get('title', item.get('title', '')),
            "snippet": translated_fields.get('snippet', item.get('snippet', '')),
            "source": translated_fields.get('source', item.get('source', ''))
        }
        
        return translated_item
        
    except Exception as e:
        print(f"Error translating item: {str(e)}")
        return item

def translate_query_to_english(query: str, model: ChatOpenAI) -> str:
    """Translate search query to English"""
    system_message = """
    You are a professional translator. Translate the following search query to English.
    
    Translation Rules:
    1. Keep the translation concise and clear
    2. Maintain the search intent
    3. Preserve any proper nouns (names, places)
    4. Keep any numbers, dates, and measurements
    5. Ensure the translation is natural and search-friendly
    
    Return ONLY the translated query without any explanations or additional text.
    """
    
    messages = [
        HumanMessage(content=f"{system_message}\n\nQuery to translate:\n{query}")
    ]
    
    try:
        response = model.invoke(messages)
        return response.content.strip()
    except Exception as e:
        print(f"Error translating query: {str(e)}")
        return query

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Global News Hub API",
        "version": "1.0.0",
        "endpoints": {
            "/languages": "Get list of supported languages",
            "/search": "Search for news articles",
            "/translate": "Translate news articles",
            "/translate-query": "Translate search query to English"
        }
    }

@app.get("/languages", response_model=List[str])
async def get_languages():
    """Get list of supported languages"""
    return SUPPORTED_LANGUAGES

@app.post("/search")
async def search_news(request: SearchRequest):
    """
    Search for news articles with optional translation
    """
    try:
        # If translation is requested and language is not English, translate query first
        search_query = request.query
        if request.translate_to and request.translate_to != "English" and request.sutra_api_key:
            model = get_chat_model(request.sutra_api_key)
            search_query = translate_query_to_english(request.query, model)
        
        # Fetch news
        news_items = fetch_news(
            query=search_query,
            num_results=request.num_results,
            serper_api_key=request.serper_api_key,
            language=request.language,
            page=request.page
        )
        
        # Translate if requested
        if request.translate_to and request.translate_to != "English" and request.sutra_api_key:
            model = get_chat_model(request.sutra_api_key)
            translated_items = []
            for item in news_items:
                translated_item = translate_news_item(item, request.translate_to, model)
                translated_items.append(translated_item)
            news_items = translated_items
        
        return {
            "success": True,
            "query": request.query,
            "translated_query": search_query if search_query != request.query else None,
            "count": len(news_items),
            "language": request.translate_to or request.language or "English",
            "news": news_items
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate")
async def translate_news(request: TranslateRequest):
    """
    Translate existing news articles to target language
    """
    try:
        if request.target_language not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail=f"Unsupported language: {request.target_language}")
        
        model = get_chat_model(request.sutra_api_key)
        translated_items = []
        
        for item in request.news_items:
            translated_item = translate_news_item(item, request.target_language, model)
            translated_items.append(translated_item)
        
        return {
            "success": True,
            "target_language": request.target_language,
            "count": len(translated_items),
            "news": translated_items
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate-query")
async def translate_query(request: TranslateQueryRequest):
    """
    Translate a search query to English
    """
    try:
        model = get_chat_model(request.sutra_api_key)
        translated_query = translate_query_to_english(request.query, model)
        
        return {
            "success": True,
            "original_query": request.query,
            "translated_query": translated_query
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 