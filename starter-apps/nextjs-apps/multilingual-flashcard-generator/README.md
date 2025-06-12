# 📚 Multilingual Flashcard Generator

A Next.js application that allows users to generate multilingual flashcards using SUTRA AI. It's designed to help language learners create and practice with flashcards in many languages.

## 🌟 Features

- Generate language learning flashcards with AI-powered translations
- Support for 20+ languages including Hindi, Gujarati, Bengali, Tamil, and many more
- Customize number of cards and content focus (vocabulary, phrases, grammar)
- Interactive flashcard review experience with flip animations
- Progress tracking to monitor your learning
- Responsive design that works on mobile and desktop

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- SUTRA API key from [Two.ai](https://www.two.ai/sutra)

### Installation

1. Clone the repository

   ```bash
   git clone https://github.com/sutra-dev/sutra-cookbook.git
   cd starter-apps/nextjs-apps/multilingual-flashcard-generator
   ```

2. Install dependencies

   ```bash
   npm install
   # or
   yarn install
   ```

3. Start the development server

   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) with your browser to use the application

## 💡 How to Use

1. Enter your SUTRA API key in the input field (or use the "Get Key" button to obtain one)
2. Input text or topic for flashcards in the text area
3. Select source and target languages from the dropdown menus
4. Adjust the number of cards you want to generate using the slider
5. Choose content focus (vocabulary, phrases, grammar)
6. Click "Generate Flashcards"
7. Use the flashcard viewer to practice with your generated cards
8. Track your progress by marking cards as "Known" or "Don't Know"

## 📋 About SUTRA

SUTRA is a powerful multilingual AI model from Two.ai that provides high-quality translations and language generation capabilities. Key features include:

- **Multilingual Support**: Handles 34+ languages including Hindi, Gujarati, Bengali, Tamil, Telugu, Kannada, Malayalam, and many international languages
- **Context-Aware Translations**: Creates translations that capture the nuance and context of the source text
- **Custom Content Focus**: Specializes translations for vocabulary learning, phrases, or grammar exercises
- **Example Generation**: Creates contextual examples to help with learning and retention

## 🧩 Project Structure

- `app/` - Next.js app router files
  - `page.tsx` - Main application page
- `components/` - React components
  - `FlashcardForm.tsx` - Form for generating flashcards
  - `FlashcardViewer.tsx` - Flashcard display and navigation
  - `ErrorMessage.tsx` - Error handling component
  - `ui/` - UI components based on shadcn/ui
- `utils/` - Utility functions
  - `flashcardGenerator.ts` - Handles API calls to SUTRA
- `types/` - TypeScript type definitions
- `constants/` - Application constants like language options
- `lib/` - Shared utilities
- `api/generate-flashcards` - Backend route to generate flashcards

## 🎨 UI/UX Features

- Modern gradient backgrounds and accents
- Interactive card flip animations
- Progress tracking with visual indicators
- Mobile-responsive design
- Accessible form controls
- Visual feedback for user actions

## 🛠️ Technologies Used

- **Frontend**: Next.js 14, React, TypeScript
- **Styling**: Tailwind CSS, shadcn/ui components
- **AI Integration**: SUTRA API
- **Icons**: Lucide React
- **Deployment**: Vercel (recommended)

## 🔮 Future Improvements

- User accounts to save flashcard sets
- Spaced repetition learning system
- Pronunciation audio for language learning
- Offline support with PWA capabilities
- Expanded language support as SUTRA evolves

## 📄 License

MIT

## 🙏 Acknowledgements

- [SUTRA LLM](https://www.two.ai/sutra) for the powerful multilingual language model
- [Next.js](https://nextjs.org) for the React framework
- [shadcn/ui](https://ui.shadcn.com) for the UI component system
- [Tailwind CSS](https://tailwindcss.com) for styling
- [Lucide](https://lucide.dev) for the beautiful icons
