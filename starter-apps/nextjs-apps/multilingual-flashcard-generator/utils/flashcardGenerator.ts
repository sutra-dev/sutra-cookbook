import { Flashcard, FlashcardGenerationParams } from "@/types";

// Call the actual API endpoint to generate flashcards
export async function generateFlashcards(
  params: FlashcardGenerationParams
): Promise<Flashcard[]> {
  const {
    inputText,
    sourceLanguage,
    targetLanguage,
    cardCount,
    focus,
    apiKey,
  } = params;

  if (!apiKey) {
    throw new Error("API key is required");
  }

  try {
    // Call the API route with the parameters
    const response = await fetch("/api/generate-flashcards", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`, // Pass API key in header
      },
      body: JSON.stringify({
        inputText,
        sourceLanguage,
        targetLanguage,
        cardCount,
        focus,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to generate flashcards");
    }

    const flashcards = await response.json();

    // Ensure we have valid flashcards with all required fields
    if (!Array.isArray(flashcards) || flashcards.length === 0) {
      throw new Error("No flashcards were generated");
    }

    // Verify and fix any flashcards missing required fields
    return flashcards.map((card, index) => ({
      id: card.id || `card-${index}`,
      front: card.front || "Missing term",
      back: card.back || "Missing translation",
      example: card.example,
    }));
  } catch (error) {
    console.error("Error generating flashcards:", error);
    throw error;
  }
}
