# Global News Hub API

A FastAPI-based REST API for fetching and translating global news in 50+ languages using Serper API for news retrieval and Sutra LLM for translations.

## Features

- 🌐 Fetch news from around the world
- 🗣️ Translate news into 50+ languages
- 🔍 Smart query translation to English for better search results
- 🖼️ Enhanced news articles with high-quality images
- ⚡ Fast and efficient REST API
- 📝 Comprehensive API documentation

## API Endpoints

- `GET /` - Welcome message and endpoint list
- `GET /languages` - Get list of supported languages
- `POST /search` - Search for news with optional translation
- `POST /translate` - Translate existing news articles
- `POST /translate-query` - Translate search query to English
- `GET /health` - Health check endpoint

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd global-news-hub
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file (optional):

```env
SERPER_API_KEY=your_serper_api_key
SUTRA_API_KEY=your_sutra_api_key
```

## Running the API

### Development mode:

```bash
uvicorn api:app --reload
```

### Production mode:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

## Usage Examples

### 1. Search for News

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "artificial intelligence",
    "num_results": 10,
    "serper_api_key": "your_serper_api_key"
  }'
```

### 2. Search with Translation

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "latest technology news",
    "num_results": 5,
    "serper_api_key": "your_serper_api_key",
    "translate_to": "Spanish",
    "sutra_api_key": "your_sutra_api_key"
  }'
```

### 3. Translate Existing News

```bash
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "news_items": [
      {
        "title": "Tech News Title",
        "snippet": "News content here",
        "source": "TechCrunch",
        "link": "https://example.com"
      }
    ],
    "target_language": "French",
    "sutra_api_key": "your_sutra_api_key"
  }'
```

### 4. Translate Query to English

```bash
curl -X POST "http://localhost:8000/translate-query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "últimas noticias de tecnología",
    "sutra_api_key": "your_sutra_api_key"
  }'
```

## Supported Languages

The API supports 50+ languages including:

- English, Hindi, Gujarati, Bengali, Tamil, Telugu, Kannada, Malayalam
- Spanish, French, German, Italian, Portuguese, Russian
- Chinese, Japanese, Korean, Arabic
- And many more...

Get the full list using: `GET /languages`

## API Keys

You'll need:

1. **Serper API Key**: Get it from [https://serper.dev/](https://serper.dev/)
2. **Sutra API Key**: Get it from [https://www.two.ai/sutra/api](https://www.two.ai/sutra/api)

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `500` - Server Error

Error responses include detailed messages:

```json
{
  "detail": "Error description here"
}
```

## CORS Configuration

The API is configured to allow all origins (`*`) for development. For production, update the CORS settings in `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Rate Limiting

Be aware of rate limits from:

- Serper API: Check your plan limits
- Sutra API: Check your plan limits

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Your License Here]
