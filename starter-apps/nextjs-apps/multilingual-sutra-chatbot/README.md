Here’s a **complete, polished `README.md`** for your project. It reflects your current setup and features, and it's written in a way that's ready to use **as-is** on GitHub:

---

````md
# 🧠 SUTRA-V2 Multilingual AI Chatbot

A modern, beautifully designed AI chatbot interface powered by **SUTRA-V2**, enabling multilingual content generation with customizable tone, length, and type — all built using **Next.js**, **Vercel AI SDK**, and **Tailwind CSS**.

---

## 🌐 Live Demo

[Click here to try the app](https://sutra-multilingual-app.vercel.app/)

---

## ✨ Features

- 🔑 API key input & verification (supports user-provided keys)
- 🌍 Multilingual content generation (choose multiple languages)
- 🎨 Tone, length, and content-type configuration (e.g., Formal, Medium, Blog)
- 💬 Real-time chat with markdown-rendered AI responses
- 🧽 Message cleanup (remove individual user/assistant turns)
- 📱 Responsive design with fixed input bar and smooth UX
- ⚡ Built using `ai/react`, `ReactMarkdown`, `lucide-react`, `Tailwind CSS`, and `Next.js`

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/sutra-chatbot.git
cd sutra-chatbot
```
````

### 2. Install dependencies

```bash
npm install
# or
yarn install
```

### 3. Run the development server

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) to see the app.

---

## 🔧 Project Structure

```bash
.
├── app/
│   ├── page.tsx           # Landing/config page
│   ├── chatbot/page.tsx   # Main chatbot interface
├── components/            # Shared UI components
├── lib/                   # API logic or helpers (if any)
├── styles/                # Tailwind and global styles
├── public/                # Static assets
└── README.md
```

---

## 🛠 Technologies Used

- **Next.js 14** with App Router
- **Vercel AI SDK** (`ai/react`)
- **Tailwind CSS** for styling
- **ReactMarkdown** for response formatting
- **Lucide-react** for icons
- **TypeScript** for type safety

---

## 🧪 Deployment

Easily deploy on **[Vercel](https://vercel.com/)**:

1. Push your repo to GitHub
2. Go to [vercel.com](https://vercel.com/)
3. Import the GitHub repo and set up environment variables (if needed)
4. Deploy 🚀

---

## 🔐 API Key Handling

- Users must provide their own **SUTRA API key**
- If missing, the app redirects them to generate or paste one
- All requests to `/api/chat` are authenticated using this key

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙌 Credits

Built with 💙 by using the awesome [SUTRA-V2](https://sutra.ai) platform.

```

---

### ✅ To Use:
- Replace `your-username` with your GitHub username
- Add screenshots in `public/screens/config.png` and `chat.png` (or remove those lines)
- Rename project folder if needed

Let me know if you'd like to:
- Add instructions for setting `.env` or serverless API routes
- Generate shields/badges (e.g., Vercel Deploy, MIT License)

I can also auto-create a `LICENSE`, `package.json`, and `vercel.json` if you're prepping for open source release.
```
