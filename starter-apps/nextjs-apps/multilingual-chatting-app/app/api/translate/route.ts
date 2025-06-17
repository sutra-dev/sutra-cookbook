import { NextRequest, NextResponse } from 'next/server'
import { OpenAI } from 'openai'

/**
 * API Route: /api/translate
 * 
 * This endpoint handles translation requests using Sutra AI.
 * It receives text to translate, target language, and API key,
 * then communicates with Sutra's API to return translated content.
 * 
 * Sutra AI is accessed through OpenAI's client library but with
 * a custom base URL pointing to Sutra's API endpoint.
 */
export async function POST(req: NextRequest) {
  try {
    // Extract parameters from the request body
    const { text, targetLanguage, sutraApiKey, stream: isStream = false } = await req.json()

    // Validate required parameters
    if (!text || !targetLanguage || !sutraApiKey) {
      return NextResponse.json(
        { error: 'Missing required parameters' },
        { status: 400 }
      )
    }

    // Create OpenAI client with Sutra API configuration
    // Note: We're using OpenAI's client library but pointing to Sutra's API
    const client = new OpenAI({
      apiKey: sutraApiKey,         // User's Sutra API key
      baseURL: 'https://api.two.ai/v2', // Sutra API endpoint
    })

    // Construct a clear prompt for the translation model
    // This asks Sutra AI to translate the text to the target language
    const prompt = `Translate the following text to ${targetLanguage}. Return only the translated text without additional commentary: "${text}" Also don't include any other text in your response.`

    // STREAMING MODE: Return translations as they're generated
    if (isStream) {
      // Set up text encoder for the streaming response
      const encoder = new TextEncoder()
      const stream = new ReadableStream({
        async start(controller) {
          try {
            // Create a streaming completion from Sutra AI
            // Using 'sutra-v2' model with temperature 0.3 for more accurate translations
            const sutraStream = await client.chat.completions.create({
              model: 'sutra-v2',
              messages: [{ role: 'user', content: prompt }],
              temperature: 0.3, // Lower temperature = more deterministic/accurate translations
              stream: true,     // Enable streaming response
            })

            // Process each chunk of the response as it arrives
            for await (const chunk of sutraStream) {
              const content = chunk.choices[0]?.delta?.content || ''
              if (content) {
                // Send each piece of content as it arrives
                controller.enqueue(encoder.encode(content))
              }
            }
            controller.close()
          } catch (error) {
            controller.error(error)
          }
        },
      })

      // Return the streaming response with appropriate headers
      return new Response(stream, {
        headers: {
          'Content-Type': 'text/plain; charset=utf-8',
          'Transfer-Encoding': 'chunked',
        },
      })
    }

    // NON-STREAMING MODE: Return complete translation in one response
    const response = await client.chat.completions.create({
      model: 'sutra-v2',        // Using Sutra's translation model
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3,         // Lower temperature for more accurate translations
    })

    // Extract the translated text from the response
    const translatedText = response.choices[0].message.content

    // Return the translated text as JSON
    return NextResponse.json({ translatedText })
    
  } catch (error) {
    // Handle errors and return appropriate response
    console.error('Translation error:', error)
    return NextResponse.json(
      { error: 'Failed to translate text' },
      { status: 500 }
    )
  }
} 