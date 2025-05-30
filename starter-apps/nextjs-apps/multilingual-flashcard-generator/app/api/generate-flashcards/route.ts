import { NextResponse } from "next/server";
import { OpenAI } from "openai";

export async function POST(req: Request) {
  try {
    // Get API key from Authorization header
    const authHeader = req.headers.get("Authorization");
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return NextResponse.json(
        { error: "API key is required in Authorization header" },
        { status: 401 }
      );
    }

    const apiKey = authHeader.substring(7); // Remove "Bearer " prefix

    // Initialize OpenAI client with the provided API key
    const client = new OpenAI({
      apiKey,
      baseURL: "https://api.two.ai/v2",
    });

    const { inputText, sourceLanguage, targetLanguage, cardCount, focus } =
      await req.json();

    const prompt = `
      Create ${cardCount} flashcards for language learning from ${sourceLanguage} to ${targetLanguage}.
      The content focus is on "${focus}".
      Use the following text as a basis: "${inputText}"
      
      For each flashcard, provide:
      1. A term or phrase in ${sourceLanguage} (front)
      2. The translation in ${targetLanguage} (back)
      3. An example sentence using the term (optional)
      
      Format the response as a JSON array of objects with the structure:
      [
        {
          "id": "1", 
          "front": "term in ${sourceLanguage}", 
          "back": "translation in ${targetLanguage}", 
          "example": "example sentence with translation"
        },
        ...
      ]
    `;

    const response = await client.chat.completions.create({
      model: "sutra-v2",
      messages: [
        {
          role: "system",
          content:
            "You are a language learning assistant that creates high-quality flashcards with accurate translations.",
        },
        {
          role: "user",
          content: prompt,
        },
      ],
      max_tokens: 1024,
      temperature: 0.7,
    });

    const content = response.choices[0].message.content;

    if (typeof content === "string") {
      // Clean up response - remove markdown code blocks if present
      const cleanedContent = content
        .replace(/```json\s*/g, "")
        .replace(/```\s*/g, "")
        .trim();

      try {
        // Try to parse the cleaned content
        const parsedContent = JSON.parse(cleanedContent);
        return NextResponse.json(parsedContent);
      } catch (parseError) {
        console.error("Failed to parse cleaned JSON response:", parseError);

        // Try to extract JSON array from the string with a more robust regex
        const jsonRegex =
          /\[\s*\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\}\s*\]/g;
        const match = cleanedContent.match(jsonRegex);

        if (match && match[0]) {
          try {
            const extractedJson = JSON.parse(match[0]);
            return NextResponse.json(extractedJson);
          } catch (innerError) {
            console.error("Failed to extract JSON array:", innerError);
          }
        }

        throw new Error("Invalid response format from AI");
      }
    }

    return NextResponse.json(
      { error: "No content returned from AI" },
      { status: 500 }
    );
  } catch (error) {
    console.error("Error generating flashcards:", error);
    return NextResponse.json(
      { error: "Failed to generate flashcards" },
      { status: 500 }
    );
  }
}
