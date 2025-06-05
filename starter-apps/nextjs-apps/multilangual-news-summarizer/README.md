# Multilingual News Summarizer

A Next.js application that summarizes news articles in multiple languages using the SUTRA AI model from TWO AI.

### [Website Link](https://multilingual-news-summarizer.vercel.app/)

## Features

- Multilingual news summarization in 50+ languages, with special support for 11+ Indian languages
- SerpAPI integration for up-to-date news information
- In-app API key management for TWO AI SUTRA and SerpAPI
- Customizable settings for search and tool call visibility
- Sample questions for easy testing
- Category and language selection shortcuts
- Responsive design for all devices

## Getting Started

### Prerequisites

- Node.js 18.x or later
- A SUTRA API key from [TWO AI](https://www.two.ai/sutra/api)
- A SerpAPI key for web search functionality

### Installation

1. Clone the repository:

```bash
git clone https://github.com/sutra-dev/sutra-cookbook.git
cd starter-apps/nextjs-apps/ multilingual-news-summarizer
```

2. Install dependencies:

```bash
npm install
```

3. Set up environment variables (optional):
   - Create a `.env.local` file in the root directory
   - Add your API keys:
   ```
   SUTRA_API_KEY=your_sutra_api_key_here
   SERP_API_KEY=your_serpapi_key_here
   ```

   Alternatively, you can add your API keys directly in the application's settings panel.

4. Run the development server:

```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Usage

1. If you haven't set environment variables, add your API keys in the settings panel (gear icon)
2. Type your news query in the text area or select a sample question
3. Use the language badges to quickly create queries in specific languages
4. Use the category badges to generate queries for specific news topics
5. Optionally, configure search settings to control SerpAPI usage
6. Click "Get Summary" to generate a news summary in your chosen language

## API Key Management

The application provides two ways to manage API keys:

1. **Environment Variables**: Set `SUTRA_API_KEY` and `SERP_API_KEY` in your `.env.local` file.

2. **In-App Settings**: Add your API keys directly in the application's settings panel:
   - Click the gear icon in the header to open settings
   - Enter your SUTRA API key from [TWO AI](https://www.two.ai/sutra/api)
   - Enter your SerpAPI key from [SerpAPI](https://serpapi.com/)
   - Keys are securely stored in your browser's localStorage

The application will display indicators in the header showing which API keys are set.

## API Routes

The application includes two main API routes:

- `/api/search` - Queries SerpAPI for recent news information
  - Accepts POST requests with a JSON body containing `query` and optional `apiKey` parameters
  - Returns news articles with title, snippet, and source information
  - Falls back to organic search results if no news results are found

- `/api/summarize` - Communicates with the SUTRA API to generate summaries
  - Accepts POST requests with a JSON body containing `query` and optional `apiKey` parameters
  - Uses TWO AI's SUTRA model (sutra-v2) to generate multilingual summaries
  - Returns the summary as plain text

## Technologies Used

- [Next.js](https://nextjs.org/) - React framework
- [React](https://reactjs.org/) - UI library
- [Tailwind CSS](https://tailwindcss.com/) - Styling
- [shadcn/ui](https://ui.shadcn.com/) - UI components
- [SUTRA API](https://www.two.ai/sutra/api) - AI model for multilingual summarization
- [SerpAPI](https://serpapi.com/) - Search functionality for recent news

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [TWO AI](https://www.two.ai/) for providing the SUTRA API
