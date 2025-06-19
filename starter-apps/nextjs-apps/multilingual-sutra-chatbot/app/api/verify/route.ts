import { streamText } from "ai";
import { createOpenAI } from "@ai-sdk/openai";

export async function POST(req: Request) {
  const { apiKey }: { apiKey?: string } = await req.json();

  if (!apiKey) {
    return new Response("Missing API Key", { status: 400 });
  }

  try {
    const sutra = createOpenAI({
      baseURL: "https://api.two.ai/v2",
      apiKey,
    });

    const result = await streamText({
      model: sutra("sutra-v2"),
      messages: [{ role: "user", content: "Ping" }],
    });

    if ("error" in result) {
      console.error("Sutra API responded with error:", result.error);
      return new Response("Invalid API Key", { status: 401 });
    }

    return new Response("Valid", { status: 200 });
  } catch (err) {
    console.error("Unexpected verification error:", err);
    return new Response("Invalid API Key", { status: 401 });
  }
}
