import { NextResponse } from "next/server"
import axios from "axios"

interface TranscriptEntry {
  text: string
  duration: number
  offset: number
  lang: string
}

interface TranscriptResponse {
  success: boolean
  transcript: TranscriptEntry[]
}

interface VideoInfo {
  channel_id: string
  category_id: string
  title: string
  thumbnail: string
  published_at: string
  view_count: string
  like_count: string
  duration: string
}

async function getVideoInfo(videoId: string, rapidApiKey: string): Promise<VideoInfo> {
  try {
    const options = {
      method: 'GET',
      url: 'https://youtube-video-information1.p.rapidapi.com/api/youtube',
      params: { video_id: videoId },
      headers: {
        'x-rapidapi-key': rapidApiKey,
        'x-rapidapi-host': 'youtube-video-information1.p.rapidapi.com'
      }
    };

    const response = await axios.request(options);
    return response.data;
  } catch (error: any) {
    console.error('Error fetching video info:', error);
    throw new Error(`Failed to fetch video information: ${error.message}`);
  }
}

async function translateText(text: string, targetLang: string, sutraApiKey: string): Promise<string> {
  try {
    const response = await fetch('https://api.two.ai/v2/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${sutraApiKey}`
      },
      body: JSON.stringify({
        model: 'sutra-v2',
        messages: [
          { 
            role: 'user', 
            content: `Translate the following text to ${targetLang}. Maintain the timestamps if present:\n\n${text}` 
          }
        ],
        temperature: 0.3,
        max_tokens: 2000
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error?.message || 'Failed to translate text');
    }

    const data = await response.json();
    return data.choices[0].message.content;
  } catch (error: any) {
    console.error('Translation error:', error);
    throw new Error(`Failed to translate: ${error.message}`);
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const { youtubeUrl, rapidApiKey, sutraApiKey, includeTimestamps, formatTranscript, targetLanguage, includeVideoInfo } = body

    // Validate YouTube URL and RapidAPI key
    if (!youtubeUrl || !rapidApiKey) {
      return NextResponse.json(
        { error: "YouTube URL and RapidAPI key are required" },
        { status: 400 }
      )
    }

    // Validate Sutra API key if translation is requested
    if (targetLanguage && !sutraApiKey) {
      return NextResponse.json(
        { error: "Sutra API key is required for translation" },
        { status: 400 }
      )
    }

    // Extract video ID from URL
    const videoId = extractVideoId(youtubeUrl)
    if (!videoId) {
      return NextResponse.json(
        { error: "Invalid YouTube URL" },
        { status: 400 }
      )
    }

    // Fetch transcript and optionally video info using RapidAPI
    const fetchPromises: Promise<any>[] = [
      // Always fetch transcript
      axios.request({
        method: "GET",
        url: "https://youtube-transcript3.p.rapidapi.com/api/transcript",
        params: { videoId },
        headers: {
          "x-rapidapi-key": rapidApiKey,
          "x-rapidapi-host": "youtube-transcript3.p.rapidapi.com",
        },
      })
    ];

    // Only fetch video info if includeVideoInfo is true
    if (includeVideoInfo) {
      fetchPromises.push(getVideoInfo(videoId, rapidApiKey));
    }

    const [transcriptResponse, ...rest] = await Promise.all(fetchPromises);
    const videoInfo = includeVideoInfo ? rest[0] : null;

    const transcriptData = transcriptResponse.data as TranscriptResponse

    if (!transcriptData.success || !transcriptData.transcript) {
      return NextResponse.json(
        { error: "Failed to fetch transcript" },
        { status: 400 }
      )
    }

    // Process the original transcript
    const originalTranscript = formatTranscriptText(
      transcriptData.transcript,
      includeTimestamps
    )

    let translatedTranscript = ""
    let translationError = ""
    
    // Translate if target language is specified and Sutra API key is provided
    if (targetLanguage && sutraApiKey) {
      try {
        translatedTranscript = await translateText(originalTranscript, targetLanguage, sutraApiKey)
      } catch (error: any) {
        console.error("Translation error:", error)
        translationError = error.message
      }
    }

    // Prepare response
    const response: any = {
      success: true,
      originalTranscript,
      translatedTranscript,
      translationError,
    }

    // Add video info to response only if it was requested and successfully fetched
    if (includeVideoInfo && videoInfo) {
      const formattedDuration = formatDuration(videoInfo.duration)
      response.videoInfo = {
        title: videoInfo.title,
        thumbnail: videoInfo.thumbnail,
        duration: formattedDuration,
        views: parseInt(videoInfo.view_count).toLocaleString(),
        likes: parseInt(videoInfo.like_count).toLocaleString(),
        publishedAt: new Date(videoInfo.published_at).toLocaleDateString(),
      }
    }

    return NextResponse.json(response)
  } catch (error: any) {
    console.error("Transcript generation error:", error)
    return NextResponse.json(
      {
        success: false,
        error:
          error.response?.data?.message ||
          error.message ||
          "Failed to generate transcript",
      },
      { status: error.response?.status || 500 }
    )
  }
}

// Helper function to extract video ID from YouTube URL
function extractVideoId(url: string): string | null {
  const regex =
    /(?:youtube\.com\/(?:[^/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?/\s]{11})/
  const match = url.match(regex)
  return match ? match[1] : null
}

// Helper function to format transcript text
function formatTranscriptText(
  transcript: TranscriptEntry[],
  includeTimestamps: boolean
): string {
  return transcript
    .map((entry) => {
      const timestamp = formatTimestamp(entry.offset)
      const text = entry.text.trim()
      return includeTimestamps ? `[${timestamp}] ${text}` : text
    })
    .join("\n")
}

// Helper function to format timestamp
function formatTimestamp(seconds: number): string {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)

  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, "0")}:${secs
      .toString()
      .padStart(2, "0")}`
  }
  return `${minutes}:${secs.toString().padStart(2, "0")}`
}

// Helper function to format duration from PT1M10S to 1:10
function formatDuration(duration: string): string {
  const match = duration.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/);
  if (!match) return "0:00";

  const [, hours, minutes, seconds] = match;
  const h = parseInt(hours || "0");
  const m = parseInt(minutes || "0");
  const s = parseInt(seconds || "0");

  if (h > 0) {
    return `${h}:${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  }
  return `${m}:${s.toString().padStart(2, "0")}`;
}
