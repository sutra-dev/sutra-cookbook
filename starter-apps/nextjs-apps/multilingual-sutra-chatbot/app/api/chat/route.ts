import { streamText, UIMessage } from "ai";
import { createOpenAI } from "@ai-sdk/openai";

export async function POST(req: Request) {
  const {
    messages,
    languages,
    tone,
    length,
    contentType,
    apiKey, // ✅ added dynamic apiKey from frontend
  }: {
    messages: UIMessage[];
    languages?: string[];
    tone?: string;
    length?: string;
    contentType?: string;
    apiKey?: string;
  } = await req.json();

  if (!apiKey) {
    return new Response("Missing API Key", { status: 401 });
  }

  const sutra = createOpenAI({
    baseURL: "https://api.two.ai/v2",
    apiKey,
  });

  // Construct the system prompt dynamically
  let systemPrompt = `You are a helpful assistant.`;

  if (languages?.length) {
    systemPrompt += ` Reply in the following languages: ${languages.join(
      ", "
    )}. Clearly separate each language's response.`;
  }

  if (tone) {
    systemPrompt += ` Use a ${tone.toLowerCase()} tone.`;
  }

  if (length) {
    systemPrompt += ` Keep the response ${length.toLowerCase()}.`;
  }

  if (contentType) {
    systemPrompt += ` Format the response as a ${contentType.toLowerCase()}.`;
  }

  const result = streamText({
    model: sutra("sutra-v2"),
    system: systemPrompt,
    messages,
  });

  return result.toDataStreamResponse();
}
