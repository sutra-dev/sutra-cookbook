'use client'

import { useState } from 'react'
import ChatInterface from '@/components/ChatInterface'
import AuthModal from '@/components/AuthModal'
import { useAuth } from '@/hooks/useAuth'

export default function HomePage() {
  const { user, token, login, logout } = useAuth()
  const [showAuth, setShowAuth] = useState(false)

  if (!user || !token) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900">
              🌐 Multilingual Budget Assistant
            </h1>
            <p className="mt-2 text-gray-600">
              Your AI-powered financial advisor supporting 50+ languages
            </p>
          </div>
          <div className="space-y-4">
            <button
              onClick={() => setShowAuth(true)}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Get Started
            </button>
          </div>
        </div>
        <AuthModal 
          isOpen={showAuth} 
          onClose={() => setShowAuth(false)}
          onLogin={login}
        />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <ChatInterface user={user} token={token} onLogout={logout} />
    </div>
  )
} 