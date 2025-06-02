# Multilingual YouTube Transcript Generator

A modern web application built with Next.js that allows users to generate and translate YouTube video transcripts into multiple languages. The application provides a clean, user-friendly interface and supports a wide range of languages.

[Live Link](https://multilingual-youtube-transcript-gen.vercel.app/)

## 🌟 Features

- 📝 Generate accurate transcripts from YouTube videos
- 🌍 Translate transcripts into 30+ languages
- ⏱️ Include/exclude timestamps in transcripts
- 📥 Download transcripts as text files
- 📋 Copy transcripts to clipboard
- 🎥 View video metadata (title, duration, views, likes)
- 🔒 Secure API key management
- 💻 Modern, responsive UI

## 🚀 Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- RapidAPI Key (for YouTube transcript generation)
- Sutra API Key (for translation features)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sutra-dev/sutra-cookbook.git

cd starter-apps/nextjs-apps/multilingual-youtube-transcript-generator
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Create a `.env.local` file in the root directory and add your API keys:
```env
NEXT_PUBLIC_RAPID_API_KEY=your_rapidapi_key
NEXT_PUBLIC_SUTRA_API_KEY=your_sutra_api_key
```

4. Start the development server:
```bash
npm run dev
# or
yarn dev
```

5. Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

## 🔧 API Configuration

### RapidAPI Setup
1. Sign up for a RapidAPI account at [RapidAPI](https://rapidapi.com/hub)
2. Subscribe to the following APIs:
   - YouTube Transcript API
   - YouTube Video Information API

### Sutra API Setup
1. Get your Sutra API key from [Two.ai](https://www.two.ai/sutra/api)
2. The API is used for high-quality translations across multiple languages

## 🌐 Supported Languages

The application supports translation to the following languages:

### Indian Languages
- Hindi (🇮🇳)
- Tamil (🇮🇳)
- Telugu (🇮🇳)
- Bengali (🇮🇳)
- Marathi (🇮🇳)
- Punjabi (🇮🇳)
- Malayalam (🇮🇳)
- Kannada (🇮🇳)
- Gujarati (🇮🇳)
- And more...

### International Languages
- English (🇬🇧)
- French (🇫🇷)
- German (🇩🇪)
- Spanish (🇪🇸)
- Japanese (🇯🇵)
- Chinese (🇨🇳)
- Russian (🇷🇺)
- Arabic (🇸🇦)
- And more...

## 🛠️ Technical Details

### API Endpoints

#### `/api/transcript`
- **Method:** POST
- **Purpose:** Generate and translate YouTube video transcripts
- **Request Body:**
```typescript
{
  youtubeUrl: string;
  includeTimestamps?: boolean;
  formatTranscript?: boolean;
  rapidApiKey: string;
  sutraApiKey?: string;
  targetLanguage?: string;
}
```
- **Response:**
```typescript
{
  success: boolean;
  originalTranscript: string;
  translatedTranscript?: string;
  translationError?: string;
  videoInfo: {
    title: string;
    thumbnail: string;
    duration: string;
    views: string;
    likes: string;
    publishedAt: string;
  };
}
```

### Key Components

- **Video Information Display:** Shows video metadata including thumbnail, title, duration, views, and likes
- **Language Selection:** Supports both predefined languages and custom language input
- **Transcript Management:** Features for copying and downloading transcripts
- **Settings Management:** Secure storage of API keys and user preferences
- **Error Handling:** Comprehensive error messages and validation

## 📱 UI Features

- Responsive design that works on desktop and mobile devices
- Modern, clean interface with intuitive controls
- Real-time loading states and feedback
- Tabbed interface for easy navigation between input and results
- Copy and download functionality for both original and translated transcripts

## 🔒 Security

- API keys are stored securely in the browser's localStorage
- Keys are never exposed in the client-side code
- All API requests are handled server-side
- Input validation and sanitization

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Next.js](https://nextjs.org/) - The React Framework
- [RapidAPI](https://rapidapi.com/) - API Marketplace
- [Two.ai](https://www.two.ai/) - Translation Services
- [shadcn/ui](https://ui.shadcn.com/) - UI Components

## 🔌 API Documentation

The application uses three main APIs to provide its functionality:

### 1. YouTube Transcript API (RapidAPI)
```typescript
Endpoint: https://youtube-transcript3.p.rapidapi.com/api/transcript
Purpose: Fetches video transcripts from YouTube videos
Method: GET

Request:
{
    params: { videoId: string },
    headers: {
        "x-rapidapi-key": string,
        "x-rapidapi-host": "youtube-transcript3.p.rapidapi.com"
    }
}

Response:
{
    success: boolean,
    transcript: Array<{
        text: string,
        duration: number,
        offset: number,
        lang: string
    }>
}
```

### 2. YouTube Video Information API (RapidAPI)
```typescript
Endpoint: https://youtube-video-information1.p.rapidapi.com/api/youtube
Purpose: Retrieves detailed metadata about YouTube videos
Method: GET

Request:
{
    params: { video_id: string },
    headers: {
        'x-rapidapi-key': string,
        'x-rapidapi-host': 'youtube-video-information1.p.rapidapi.com'
    }
}

Response:
{
    channel_id: string,
    category_id: string,
    title: string,
    thumbnail: string,
    published_at: string,
    view_count: string,
    like_count: string,
    duration: string
}
```

### 3. Sutra Translation API (Two.ai)
```typescript
Endpoint: https://api.two.ai/v2/chat/completions
Purpose: Handles translation of transcripts into multiple languages
Method: POST

Request:
{
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ${sutraApiKey}'
    },
    body: {
        model: 'sutra-v2',
        messages: [
            {
                role: 'user',
                content: string // Translation prompt
            }
        ],
        temperature: 0.3,
        max_tokens: 2000
    }
}

Response:
{
    choices: [{
        message: {
            content: string // Translated text
        }
    }]
}
```

### API Integration Flow

1. When a user submits a YouTube URL:
   - The application extracts the video ID
   - Fetches video information using the YouTube Video Information API
   - Simultaneously retrieves the transcript using the YouTube Transcript API

2. If translation is requested:
   - The original transcript is processed and formatted
   - Sent to the Sutra Translation API with the target language
   - Translated content is returned and displayed alongside the original

3. Error Handling:
   - Each API call is wrapped in try-catch blocks
   - Specific error messages for different failure scenarios
   - Graceful degradation when translation fails

## 📝 API Examples

### 1. YouTube Transcript API Example

```typescript
// Example Request
const videoId = "dQw4w9WgXcQ";  // From URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ

const response = await axios.request({
    method: "GET",
    url: "https://youtube-transcript3.p.rapidapi.com/api/transcript",
    params: { videoId },
    headers: {
        "x-rapidapi-key": "your-rapidapi-key",
        "x-rapidapi-host": "youtube-transcript3.p.rapidapi.com",
    },
});

// Example Response
{
    "success": true,
    "transcript": [
        {
            "text": "We're no strangers to love",
            "duration": 4.48,
            "offset": 0.32,
            "lang": "en"
        },
        {
            "text": "You know the rules and so do I",
            "duration": 3.84,
            "offset": 4.8,
            "lang": "en"
        }
        // ... more transcript entries
    ]
}
```

### 2. YouTube Video Information API Example

```typescript
// Example Request
const videoId = "dQw4w9WgXcQ";

const response = await axios.request({
    method: 'GET',
    url: 'https://youtube-video-information1.p.rapidapi.com/api/youtube',
    params: { video_id: videoId },
    headers: {
        'x-rapidapi-key': 'your-rapidapi-key',
        'x-rapidapi-host': 'youtube-video-information1.p.rapidapi.com'
    }
});

// Example Response
{
    "channel_id": "UCuAXFkgsw1L7xaCfnd5JJOw",
    "title": "Rick Astley - Never Gonna Give You Up (Official Music Video)",
    "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
    "published_at": "2009-10-25T06:57:33Z",
    "view_count": "1234567890",
    "like_count": "12345678",
    "duration": "PT3M32S"  // ISO 8601 duration format
}
```

### 3. Sutra Translation API Example

```typescript
// Example Request
const response = await fetch('https://api.two.ai/v2/chat/completions', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer your-sutra-api-key'
    },
    body: JSON.stringify({
        model: 'sutra-v2',
        messages: [
            {
                role: 'user',
                content: 'Translate the following text to Hindi:\n\n[0:00] We\'re no strangers to love\n[0:04] You know the rules and so do I'
            }
        ],
        temperature: 0.3,
        max_tokens: 2000
    })
});

// Example Response
{
    "choices": [
        {
            "message": {
                "content": "[0:00] हम प्यार के अजनबी नहीं हैं\n[0:04] आप नियम जानते हैं और मैं भी",
                "role": "assistant"
            }
        }
    ],
    "usage": {
        "prompt_tokens": 37,
        "completion_tokens": 42,
        "total_tokens": 79
    }
}
```

### Common Error Responses

#### 1. Invalid or Missing API Key
```json
{
    "success": false,
    "error": {
        "message": "Invalid API key provided",
        "status": 401
    }
}
```

#### 2. Video Not Found
```json
{
    "success": false,
    "error": {
        "message": "The requested video could not be found",
        "status": 404
    }
}
```

#### 3. Translation Error
```json
{
    "success": false,
    "error": {
        "message": "Failed to translate: Text too long or unsupported language",
        "status": 400
    }
}
```

### Rate Limiting

1. **RapidAPI (YouTube APIs)**
   - Basic Plan: 100 requests/day
   - Pro Plan: 10,000 requests/day
   - Response Headers:
     ```
     x-ratelimit-requests-limit: 100
     x-ratelimit-requests-remaining: 85
     ```

2. **Sutra API (Translation)**
   - Standard Plan: 100,000 tokens/month
   - Response includes token usage:
     ```json
     {
         "usage": {
             "prompt_tokens": 37,
             "completion_tokens": 42,
             "total_tokens": 79
         }
     }
     ```

### Testing the APIs

You can use the following test video IDs for development:
```typescript
const TEST_VIDEO_IDS = [
    "dQw4w9WgXcQ",  // English video with captions
    "jNQXAC9IVRw",  // Short video
    "8jPQjjsBbIc",  // Multi-language video
];
```

### Error Handling Best Practices

```typescript
try {
    // 1. Validate video ID before making API calls
    const videoId = extractVideoId(youtubeUrl);
    if (!videoId) throw new Error("Invalid YouTube URL");

    // 2. Check API key presence
    if (!rapidApiKey) throw new Error("RapidAPI key is required");
    if (targetLanguage && !sutraApiKey) throw new Error("Sutra API key is required for translation");

    // 3. Make API calls with timeout
    const response = await Promise.race([
        fetchTranscript(videoId),
        new Promise((_, reject) => 
            setTimeout(() => reject(new Error("Request timeout")), 10000)
        )
    ]);

    // 4. Handle successful response
    if (response.success) {
        // Process transcript
    }
} catch (error) {
    // 5. Handle specific error types
    if (error.response?.status === 429) {
        console.error("Rate limit exceeded");
    } else if (error.response?.status === 404) {
        console.error("Video not found or no captions available");
    } else {
        console.error("Unexpected error:", error.message);
    }
}
```
