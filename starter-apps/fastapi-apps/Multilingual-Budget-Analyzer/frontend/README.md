# Multilingual Budget Assistant - Frontend

A modern NextJS frontend for the multilingual budget assistant with ChatGPT-like interface.

## Features

- 🌐 **Multilingual Support** - Supports 50+ languages via Sutra LLM
- 💬 **ChatGPT-like Interface** - Modern, responsive chat UI
- 📄 **Document Upload** - Upload receipts, bank statements, PDFs for AI analysis
- 🔐 **Authentication** - Secure JWT-based auth
- 📱 **Responsive Design** - Works on desktop and mobile
- 🎨 **Modern UI** - Built with Tailwind CSS and Lucide icons

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **File Upload**: React Dropzone
- **Charts**: Plotly.js (ready for future analytics)

## Setup Instructions

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Environment Setup**
   The frontend proxies API calls to the FastAPI backend at `http://localhost:8000`
   Make sure your FastAPI backend is running first.

3. **Start development server**
   ```bash
   npm run dev
   ```
   
   Open [http://localhost:3000](http://localhost:3000) in your browser.

4. **Build for production**
   ```bash
   npm run build
   npm start
   ```

## Project Structure

```
frontend/
├── app/                 # Next.js App Router pages
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Main chat page
│   └── globals.css     # Global styles
├── components/         # React components
│   ├── ChatInterface.tsx  # Main chat interface
│   └── AuthModal.tsx      # Login/register modal
├── hooks/              # Custom React hooks
│   └── useAuth.ts      # Authentication logic
├── next.config.js      # Next.js config with API proxy
├── tailwind.config.js  # Tailwind CSS config
└── tsconfig.json       # TypeScript config
```

## API Integration

The frontend connects to these FastAPI endpoints:

- `POST /auth/login` - User authentication
- `POST /auth/register` - User registration  
- `GET /auth/me` - Get current user
- `POST /ai/get-advice` - Get financial advice
- `POST /ai/upload-document` - Upload and analyze documents

## Usage

1. **Authentication**: Click "Get Started" to login or register
2. **Chat**: Type financial questions or click suggested prompts
3. **File Upload**: Click the upload button to analyze receipts/statements
4. **Multilingual**: The AI responds in your preferred language (set during registration)

## Development Notes

- The app uses Next.js API rewrites to proxy `/api/*` to `http://localhost:8000`
- Authentication tokens are stored in localStorage
- File uploads support PDF, PNG, JPG, JPEG, BMP, TIFF formats
- Real-time chat interface with typing indicators

## Future Enhancements

- Interactive Plotly charts for spending analytics
- Transaction management interface
- Portfolio performance tracking
- Dark mode support 