# Global News Hub Frontend

A modern, responsive Next.js frontend for the Global News Hub - a multilingual news platform that fetches and translates news in 50+ languages.

## 🎨 Design Features

- **Modern UI**: Clean, minimalist design with smooth animations
- **Dark Mode Ready**: Full dark mode support with CSS variables
- **Responsive**: Works perfectly on mobile, tablet, and desktop
- **Glass Morphism**: Beautiful glass effect on the header
- **Animated Cards**: Hover effects and transitions on news cards
- **Skeleton Loading**: Smooth loading states for better UX

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ installed
- The FastAPI backend running on `http://localhost:8000`

### Installation

1. Navigate to the frontend directory:

```bash
cd news-hub-frontend
```

2. Install dependencies:

```bash
npm install
```

3. Create a `.env.local` file with your API keys:

```env
# Backend API URL (optional, defaults to http://localhost:8000)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Serper API Key (required)
# Get yours at: https://serper.dev/
NEXT_PUBLIC_SERPER_API_KEY=your_serper_api_key_here

# Sutra API Key (optional, needed for translations)
# Get yours at: https://www.two.ai/sutra/api
NEXT_PUBLIC_SUTRA_API_KEY=your_sutra_api_key_here
```

4. Make sure the backend API is running:

```bash
# In the parent directory
cd ..
uvicorn api:app --reload
```

5. Run the development server:

```bash
npm run dev
```

6. Open [http://localhost:3000](http://localhost:3000) in your browser

## 🔧 Configuration

### API Keys

Configure your API keys in the `.env.local` file:

- **NEXT_PUBLIC_SERPER_API_KEY**: Required for fetching news
- **NEXT_PUBLIC_SUTRA_API_KEY**: Optional, needed for translations to non-English languages

### Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL (default: `http://localhost:8000`)
- `NEXT_PUBLIC_SERPER_API_KEY`: Your Serper API key
- `NEXT_PUBLIC_SUTRA_API_KEY`: Your Sutra API key (optional)

## 📁 Project Structure

```
news-hub-frontend/
├── app/
│   ├── globals.css         # Global styles and Tailwind config
│   ├── layout.tsx          # Root layout with metadata
│   └── page.tsx            # Main homepage
├── components/
│   ├── ui/                 # Reusable UI components
│   │   ├── button.tsx      # Button component
│   │   └── card.tsx        # Card components
│   ├── news-card.tsx       # News article card
│   └── news-card-skeleton.tsx # Loading skeleton
├── lib/
│   ├── api.ts              # API service layer
│   └── utils.ts            # Utility functions
└── public/                 # Static assets
```

## 🎨 Customization

### Theme Colors

Edit the CSS variables in `app/globals.css`:

```css
:root {
  --primary: 199 89% 48%;  /* Sky blue */
  --background: 0 0% 100%;  /* White */
  --foreground: 222.2 84% 4.9%; /* Dark text */
}
```

### Animations

Custom animations are defined in:

- `tailwind.config.ts` - Keyframe animations
- `app/globals.css` - Component-specific animations

## 🧪 Development

### Running Tests

```bash
npm test
```

### Building for Production

```bash
npm run build
npm start
```

### Linting

```bash
npm run lint
```

## 🚀 Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Import the project in Vercel
3. Set the environment variable:
   - `NEXT_PUBLIC_API_URL`: Your production API URL
4. Deploy!

### Docker

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.
