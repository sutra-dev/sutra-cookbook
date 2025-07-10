'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Upload, LogOut, User, Bot } from 'lucide-react'

interface User {
  id: string
  email: string
  preferred_language: string
  currency: string
}

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface ChatInterfaceProps {
  user: User
  token: string
  onLogout: () => void
}

export default function ChatInterface({ user, token, onLogout }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [conversationId, setConversationId] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() && !selectedFile) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input || `Uploaded: ${selectedFile?.name}`,
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setLoading(true)
    setInput('')

    try {
      let response
      
      if (selectedFile) {
        // Handle file upload
        const formData = new FormData()
        formData.append('file', selectedFile)
        if (conversationId) {
          formData.append('conversation_id', conversationId)
        }

        response = await fetch('/api/ai/upload-document', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
          body: formData,
        })
      } else {
        // Handle text message
        response = await fetch('/api/ai/get-advice', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({
            message: input,
            conversation_id: conversationId,
          }),
        })
      }

      if (response.ok) {
        const data = await response.json()
        
        // Update conversation ID if provided
        if (data.conversation_id) {
          setConversationId(data.conversation_id)
        }
        
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: selectedFile ? data.ai_advice : data.answer,
          timestamp: new Date(),
        }
        setMessages(prev => [...prev, assistantMessage])
        
        // If file upload, add insights as a separate message
        if (selectedFile && data.insights && data.insights.length > 0) {
          const insightsMessage: Message = {
            id: (Date.now() + 2).toString(),
            role: 'assistant',
            content: `📊 **Document Analysis Insights:**\n\n${data.insights.join('\n')}\n\n**File Type:** ${data.file_type}\n**File Size:** ${(data.file_size / 1024).toFixed(1)} KB`,
            timestamp: new Date(),
          }
          setMessages(prev => [...prev, insightsMessage])
        }
      } else {
        throw new Error('Failed to get response')
      }
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
      setSelectedFile(null)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setSelectedFile(file)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-4 py-3 flex justify-between items-center">
        <div>
          <h1 className="text-lg font-semibold text-gray-900">
            🌐 Multilingual Budget Assistant
          </h1>
          <p className="text-sm text-gray-600">
            Auto-detects language • {user.email}
            {conversationId && (
              <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                💬 Context Active
              </span>
            )}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {conversationId && (
            <button
              onClick={() => {
                setConversationId(null)
                setMessages([])
              }}
              className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-gray-900 transition-colors"
              title="Start New Conversation"
              aria-label="Start new conversation"
            >
              <Bot size={16} />
              New Chat
            </button>
          )}
          <button
            onClick={onLogout}
            className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-gray-900 transition-colors"
            title="Logout"
            aria-label="Logout from application"
          >
            <LogOut size={16} />
            Logout
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <Bot size={48} className="mx-auto mb-4 text-gray-400" />
            <h3 className="text-lg font-medium mb-2">Welcome to your AI Financial Advisor!</h3>
            <p className="text-sm">
              Ask me anything about budgeting, investments, or upload financial documents for analysis.
            </p>
            <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-md mx-auto">
              <button
                onClick={() => setInput("Give me tips to save 20% of my income")}
                className="p-2 text-left text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
              >
                💰 Saving tips
              </button>
              <button
                onClick={() => setInput("How should I diversify my investment portfolio?")}
                className="p-2 text-left text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
              >
                📈 Investment advice
              </button>
              <button
                onClick={() => setInput("Help me create a monthly budget")}
                className="p-2 text-left text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
              >
                📊 Budget planning
              </button>
              <button
                onClick={() => fileInputRef.current?.click()}
                className="p-2 text-left text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
              >
                📄 Upload document
              </button>
            </div>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[70%] rounded-lg px-4 py-2 ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-900 border border-gray-200'
              }`}
            >
              <div className="flex items-start gap-2">
                {message.role === 'assistant' && (
                  <Bot size={16} className="mt-1 flex-shrink-0 text-gray-600" />
                )}
                {message.role === 'user' && (
                  <User size={16} className="mt-1 flex-shrink-0 text-blue-200" />
                )}
                <div className="flex-1">
                  <p className="whitespace-pre-wrap">{message.content}</p>
                  <p className={`text-xs mt-1 ${
                    message.role === 'user' ? 'text-blue-200' : 'text-gray-500'
                  }`}>
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                </div>
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-lg px-4 py-2 max-w-[70%]">
              <div className="flex items-center gap-2">
                <Bot size={16} className="text-gray-600" />
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce animate-bounce-delay-1"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce animate-bounce-delay-2"></div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="bg-white border-t border-gray-200 p-4">
        {selectedFile && (
          <div className="mb-2 p-2 bg-blue-50 border border-blue-200 rounded-lg flex items-center justify-between">
            <span className="text-sm text-blue-700">📎 {selectedFile.name}</span>
            <button
              onClick={() => setSelectedFile(null)}
              className="text-blue-700 hover:text-blue-900"
              title="Remove selected file"
              aria-label="Remove selected file"
            >
              ✕
            </button>
          </div>
        )}
        
        <div className="flex items-end gap-2">
          <div className="flex-1 min-h-[40px] max-h-32 border border-gray-300 rounded-lg overflow-hidden">
            <label htmlFor="message-input" className="sr-only">
              Type your financial question or message
            </label>
            <textarea
              id="message-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about your finances or upload a document..."
              className="w-full h-full px-3 py-2 resize-none focus:outline-none"
              rows={1}
              title="Type your financial question or message"
              aria-label="Type your financial question or message"
            />
          </div>
          
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.doc,.docx,.xlsx,.xls,.csv,.png,.jpg,.jpeg,.bmp,.tiff"
            onChange={handleFileSelect}
            className="hidden"
            id="file-upload"
            title="Upload file"
            aria-label="Upload file (PDF, DOC, DOCX, XLSX, XLS, CSV, PNG, JPG, JPEG, BMP, TIFF)"
          />
          
          <button
            onClick={() => fileInputRef.current?.click()}
            className="p-2 text-gray-500 hover:text-gray-700 transition-colors"
            disabled={loading}
            title="Upload file"
            aria-label="Upload file"
          >
            <Upload size={20} />
          </button>
          
          <button
            onClick={sendMessage}
            disabled={loading || (!input.trim() && !selectedFile)}
            className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            title="Send message"
            aria-label="Send message"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  )
} 