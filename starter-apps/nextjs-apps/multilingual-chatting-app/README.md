# Multilingual Chat App

A real-time chat application that breaks language barriers using [Sutra AI](https://www.two.ai/sutra/api) translation. Connect with anyone worldwide by chatting in your preferred language while they read in theirs.

Deployed Link : https://multilingual-chatting-app.vercel.app/
## ✨ Features

- **Real-time messaging** powered by Supabase Realtime
- **Instant translations** between 10+ languages using Sutra AI
- **Create or join** private chat rooms with unique session IDs
- **No account needed** - just enter a name and start chatting
- **User presence tracking** shows who's currently in the chat
- **Modern, responsive UI** built with shadcn/ui components

## 🤖 About Sutra AI

[Sutra AI](https://www.two.ai/sutra/api) is the translation engine that powers this application:

- **High-quality translations** across multiple languages
- **Context-aware** translations that maintain meaning and tone
- **Simple API integration** through OpenAI-compatible endpoints

To use the translation features in this app, you'll need a Sutra API key from [two.ai](https://www.two.ai/sutra/api).

## 🚀 Getting Started

### Prerequisites

- [Node.js 18+](https://nodejs.org/)
- [Supabase](https://supabase.io/) account (free tier available)
- [Sutra AI API key](https://www.two.ai/sutra/api) for translations

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sutra-dev/sutra-cookbook.git
   cd starter-apps/nextjs-apps/multilingual-chatting-app
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create a `.env.local` file** with your Supabase credentials:
   ```
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

4. **Set up the Supabase database table** by running this SQL in your Supabase SQL editor:
   ```sql
   CREATE TABLE multilingual_chat (
     id SERIAL PRIMARY KEY,
     sessionid UUID NOT NULL UNIQUE,
     users JSONB DEFAULT '[]'::jsonb,
     msgs JSONB DEFAULT '[]'::jsonb,
     created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
     last_activity TIMESTAMP WITH TIME ZONE DEFAULT now()
   );
   ```

5. **Enable Realtime** for the `multilingual_chat` table in your Supabase dashboard

6. **Run the development server**
   ```bash
   npm run dev
   ```

7. **Open [http://localhost:3000](http://localhost:3000)** in your browser

## 📱 Using the App

1. On first launch, click the **Settings** button and enter your Sutra API key
2. Choose to **Create a Room** or **Join a Room** with an existing session ID
3. Enter your display name
4. Start chatting!
5. Use the language selector (globe icon) to change the display language

## 🧩 How Sutra AI Integration Works

This app uses Sutra AI for real-time translations through the following process:

1. **API Configuration**: The app connects to Sutra AI using the OpenAI client library but with a custom base URL pointing to Sutra's API endpoint.

2. **Translation Logic**: When a user selects a language other than "Original":
   - The app fetches translations for all messages in the selected language
   - New translations are cached to avoid repeated API calls
   - Messages appear in the user's chosen language

3. **API Implementation**: 
   - The `/api/translate` endpoint handles secure communication with Sutra
   - Messages are sent with a prompt requesting translation to the target language
   - Both streaming and non-streaming modes are supported

4. **Code Implementation**:
   ```typescript
   // Example of how translation is requested
   const translateMessage = async (text, targetLang) => {
     // API call to /api/translate endpoint
     const response = await fetch("/api/translate", {
       method: "POST",
       headers: { "Content-Type": "application/json" },
       body: JSON.stringify({
         text,
         targetLanguage: targetLang, 
         sutraApiKey,
         stream: false,
       }),
     });
     
     // Process and return translated text
     const data = await response.json();
     return data.translatedText;
   }
   ```

## 🔧 Project Structure

- `/app/page.tsx` - Home page with room creation/joining UI
- `/app/chat/[sessionID]/page.tsx` - Chat room with messaging and translation
- `/app/api/translate/route.ts` - API route for Sutra AI translation
- `/lib/supabase/client.ts` - Supabase client initialization
- `/components/ui/...` - UI components from shadcn/ui

## 🛠️ Technology Stack

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Backend**: Next.js API Routes, Supabase
- **Database**: Supabase Postgres with Realtime subscriptions
- **UI Components**: shadcn/ui (based on Radix UI)
- **Translation**: Sutra AI via OpenAI-compatible API
- **Animations**: Framer Motion

## 📄 License

MIT
