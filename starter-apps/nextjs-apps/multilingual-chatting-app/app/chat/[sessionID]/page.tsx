"use client"

/**
 * Multilingual Chat Room Component
 * 
 * This component implements a real-time chat room with multilingual translation capabilities
 * powered by Sutra AI. The translation workflow works as follows:
 * 
 * 1. User Authentication:
 *    - Users enter the room with a username via URL query params
 *    - A Sutra API key is required for translation (stored in localStorage)
 * 
 * 2. Translation System:
 *    - Users select their preferred language from the dropdown
 *    - When a non-original language is selected, all messages are translated
 *    - Translations are cached to avoid redundant API calls
 *    - The translation process happens in the background and shows a loading indicator
 * 
 * 3. Sutra AI Integration:
 *    - Translation requests are sent to our Next.js API endpoint (/api/translate)
 *    - The API endpoint communicates with Sutra AI using user's API key
 *    - Sutra translates text to the requested language and returns results
 *    - Translated text is displayed in the chat interface
 * 
 * 4. Translation Cache:
 *    - Each message translation is stored with a unique key: messageId-languageCode
 *    - The cache prevents re-translating the same message multiple times
 *    - When switching languages, only untranslated messages are sent for translation
 */

import { useState, useEffect, useRef } from "react"
import { useRouter, useParams, useSearchParams } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Label } from "@/components/ui/label"
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { Settings, MessageSquare, ArrowLeft, Send, Globe, Copy, Check, Users, Loader2 } from "lucide-react"
import { createClient } from '@supabase/supabase-js'
import { motion } from 'framer-motion'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

// Define message types
type Message = {
  id: string
  username: string
  text: string
  timestamp: number
  translated?: boolean
}

// Define translation cache type
type TranslationCache = Record<string, string>;

// Language options
const LANGUAGES = [
  { name: "Original", code: "original" },
  // Indian languages (7)
  { name: "Hindi", code: "hi", flag: "🇮🇳" },
  { name: "Tamil", code: "ta", flag: "🇮🇳" },
  { name: "Bengali", code: "bn", flag: "🇮🇳" },
  { name: "Telugu", code: "te", flag: "🇮🇳" },
  { name: "Marathi", code: "mr", flag: "🇮🇳" },
  { name: "Gujarati", code: "gu", flag: "🇮🇳" },
  { name: "Kannada", code: "kn", flag: "🇮🇳" },
  // Foreign languages (3)
  { name: "English", code: "en", flag: "🇬🇧" },
  { name: "Spanish", code: "es", flag: "🇪🇸" },
  { name: "Chinese", code: "zh", flag: "🇨🇳" },
]

// Initialize Supabase client
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || ''
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''
const supabase = createClient(supabaseUrl, supabaseKey)

export default function ChatRoom() {
  const router = useRouter()
  const params = useParams()
  const searchParams = useSearchParams()
  const sessionID = params.sessionID as string
  const username = searchParams.get("username") || "Anonymous"
  
  const [messages, setMessages] = useState<Message[]>([])
  const [translationCache, setTranslationCache] = useState<TranslationCache>({})
  const [newMessage, setNewMessage] = useState("")
  const [users, setUsers] = useState<string[]>([])
  const [language, setLanguage] = useState("original")
  const [sutraApiKey, setSutraApiKey] = useState("")
  const [copied, setCopied] = useState(false)
  const [isTranslating, setIsTranslating] = useState(false)
  const [sendingMessage, setSendingMessage] = useState(false)
  const [showUsersPanel, setShowUsersPanel] = useState(false)
  const [customLanguage, setCustomLanguage] = useState("")
  const [customLanguageCode, setCustomLanguageCode] = useState("")
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Load API key from localStorage
  useEffect(() => {
    const savedKey = localStorage.getItem("sutraApiKey")
    if (savedKey) setSutraApiKey(savedKey)
    
    // Join the chat room
    joinChatRoom()
    
    // Set up real-time subscription
    setupRealtimeSubscription()
    
    // Add user to the room
    addUserToRoom()
    
    // Cleanup on unmount
    return () => {
      // Remove user from room when they leave
      removeUserFromRoom()
    }
  }, [sessionID, username])

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Handle translations when language changes or new messages arrive
  useEffect(() => {
    // Skip if using original language or no API key
    if (language === "original" || !sutraApiKey) return
    
    // Check if we need to do any translations
    // by finding messages that haven't been translated to the current language yet
    let needsTranslation = false;
    for (const message of messages) {
      const cacheKey = `${message.id}-${language}`;
      if (!translationCache[cacheKey]) {
        needsTranslation = true;
        break;
      }
    }
    
    if (!needsTranslation) return;
    
    // Create a function to translate untranslated messages
    const translateUntranslatedMessages = async () => {
      setIsTranslating(true) // Show translation loading indicator
      
      try {
        // For each message that needs translation
        const newTranslations: TranslationCache = {};
        const promises: Promise<void>[] = [];
        
        for (const message of messages) {
          const cacheKey = `${message.id}-${language}`;
          
          // Skip if already in cache to avoid unnecessary API calls
          if (translationCache[cacheKey]) continue;
          
          // Queue up translation promises for parallel processing
          promises.push(
            translateMessage(message.text, language)
              .then(translatedText => {
                // Store result in the new translations object
                newTranslations[cacheKey] = translatedText;
              })
              .catch(error => {
                console.error(`Translation error for message ${message.id}:`, error);
              })
          );
        }
        
        // Wait for all translations to complete simultaneously
        await Promise.all(promises);
        
        // Only update cache if we have new translations
        if (Object.keys(newTranslations).length > 0) {
          // Update translation cache with all new translations at once
          setTranslationCache(prev => ({
            ...prev,
            ...newTranslations
          }));
        }
      } finally {
        setIsTranslating(false) // Hide translation loading indicator
      }
    };
    
    translateUntranslatedMessages();
  }, [language, messages, sutraApiKey, translationCache]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  // Join chat room and load existing messages
  const joinChatRoom = async () => {
    try {
      // Check if room exists
      const { data: room } = await supabase
        .from('multilingual_chat')
        .select('*')
        .eq('sessionid', sessionID)
        .single()
      
      if (room) {
        // Load messages
        setMessages(room.msgs || [])
        // Load users
        setUsers(room.users || [])
      } else {
        // Create new room if it doesn't exist
        await supabase
          .from('multilingual_chat')
          .insert([
            {
              sessionid: sessionID,
              users: [username],
              msgs: [],
              created_at: new Date().toISOString()
            }
          ])
        
        setUsers([username])
      }
    } catch (error) {
      console.error('Error joining room:', error)
    }
  }

  // Set up real-time subscription to the chat room
  const setupRealtimeSubscription = () => {
    const channel = supabase
      .channel(`room:${sessionID}`)
      .on('postgres_changes', { 
        event: 'UPDATE', 
        schema: 'public', 
        table: 'multilingual_chat',
        filter: `sessionid=eq.${sessionID}` 
      }, (payload) => {
        if (payload.new) {
          const newData = payload.new as any
          setMessages(newData.msgs || [])
          setUsers(newData.users || [])
        }
      })
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }

  // Add user to the room
  const addUserToRoom = async () => {
    try {
      const { data: room } = await supabase
        .from('multilingual_chat')
        .select('users')
        .eq('sessionid', sessionID)
        .single()
      
      if (room) {
        const existingUsers = room.users || []
        if (!existingUsers.includes(username)) {
          const updatedUsers = [...existingUsers, username]
          
          await supabase
            .from('multilingual_chat')
            .update({ users: updatedUsers })
            .eq('sessionid', sessionID)
        }
      }
    } catch (error) {
      console.error('Error adding user to room:', error)
    }
  }

  // Remove user from room
  const removeUserFromRoom = async () => {
    try {
      const { data: room } = await supabase
        .from('multilingual_chat')
        .select('users')
        .eq('sessionid', sessionID)
        .single()
      
      if (room) {
        const updatedUsers = (room.users || []).filter((user: string) => user !== username)
        
        await supabase
          .from('multilingual_chat')
          .update({ users: updatedUsers })
          .eq('sessionid', sessionID)
      }
    } catch (error) {
      console.error('Error removing user from room:', error)
    }
  }

  // Send a message to the chat room
  const sendMessage = async () => {
    if (!newMessage.trim() || sendingMessage) return
    
    try {
      setSendingMessage(true)
      
      const messageId = crypto.randomUUID()
      const newMsg: Message = {
        id: messageId,
        username,
        text: newMessage,
        timestamp: Date.now()
      }
      
      const { data: room, error: selectError } = await supabase
        .from('multilingual_chat')
        .select('msgs')
        .eq('sessionid', sessionID)
        .single()
      
      if (selectError) {
        console.error("Error fetching room:", selectError)
        alert(`Error fetching room: ${selectError.message}`)
        return
      }
      
      const existingMessages = room?.msgs || []
      const updatedMessages = [...existingMessages, newMsg]
      
      const { error: updateError } = await supabase
        .from('multilingual_chat')
        .update({ msgs: updatedMessages })
        .eq('sessionid', sessionID)
      
      if (updateError) {
        console.error("Error updating room:", updateError)
        alert(`Error sending message: ${updateError.message}`)
        return
      }
      
      setNewMessage("")
    } catch (error) {
      console.error('Error sending message:', error)
      alert(`Unexpected error: ${error instanceof Error ? error.message : String(error)}`)
    } finally {
      setSendingMessage(false)
    }
  }

  // Translate messages using Sutra API via OpenAI client
  const translateMessage = async (text: string, targetLang: string) => {
    // Skip translation if no API key is available or original language is selected
    if (!sutraApiKey || targetLang === "original") return text
    
    try {
      // Call our Next.js API endpoint which handles communication with Sutra AI
      // This keeps the Sutra API key secure on the server side
      const response = await fetch("/api/translate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text,              // The text to be translated
          targetLanguage: targetLang,  // The language code to translate to (e.g., 'es', 'zh', 'hi')
          sutraApiKey,       // The user's Sutra API key stored in local storage
          stream: false,     // Whether to stream the translation (false for simpler implementation)
        }),
      })
      
      // Check if the request was successful
      if (!response.ok) {
        throw new Error("Translation failed")
      }
      
      // Extract the translated text from the response
      const data = await response.json()
      return data.translatedText
    } catch (error) {
      console.error("Translation error:", error)
      // Return original text with error indicator if translation fails
      return text + " (translation failed)"
    }
  }

  // Get displayed message text (translated or original)
  const getMessageText = (message: Message) => {
    // If using original language, just return the original message
    if (language === "original") return message.text
    
    // Look up the translation in our cache using a unique key combination of message ID and target language
    const cacheKey = `${message.id}-${language}`
    // Return the cached translation if available, otherwise return original text
    // (translation might still be in progress)
    return translationCache[cacheKey] || message.text
  }

  // Handle copy session ID
  const copySessionId = () => {
    navigator.clipboard.writeText(sessionID)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  // Format timestamp
  const formatTime = (timestamp: number) => {
    return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }
  
  // Get active language info
  const getActiveLanguage = () => {
    return LANGUAGES.find(lang => lang.code === language) || LANGUAGES[0]
  }

  // Create avatar colors based on username
  const getUserAvatarColor = (userName: string) => {
    const colors = [
      "bg-indigo-500", "bg-blue-500", "bg-green-500", 
      "bg-amber-500", "bg-rose-500", "bg-purple-500", 
      "bg-teal-500", "bg-cyan-500", "bg-pink-500"
    ]
    
    // Simple hash function to get consistent color for same username
    let hash = 0;
    for (let i = 0; i < userName.length; i++) {
      hash = userName.charCodeAt(i) + ((hash << 5) - hash);
    }
    
    const index = Math.abs(hash) % colors.length;
    return colors[index];
  }

  // Add custom language to the languages list
  const addCustomLanguage = () => {
    if (customLanguage && customLanguageCode) {
      setLanguage(customLanguageCode)
      // Don't add duplicates
      if (!LANGUAGES.some(lang => lang.code === customLanguageCode)) {
        LANGUAGES.push({ name: customLanguage, code: customLanguageCode, flag: "🌐" })
      }
      setCustomLanguage("")
      setCustomLanguageCode("")
    }
  }

  return (
    <div className="flex h-screen overflow-hidden bg-slate-50">
      {/* Sidebar for users (mobile: sheet, desktop: sidebar) */}
      <Sheet open={showUsersPanel} onOpenChange={setShowUsersPanel}>
        <SheetContent side="left" className="w-full max-w-sm p-0">
          <div className="flex h-full flex-col">
            <SheetHeader className="px-6 py-4 border-b">
              <SheetTitle className="text-lg font-semibold">Active Users</SheetTitle>
              <SheetDescription>
                {users.length} {users.length === 1 ? 'participant' : 'participants'} in this chat
              </SheetDescription>
            </SheetHeader>
            <div className="flex-1 overflow-y-auto p-6">
              <div className="space-y-4">
                {users.map((user, index) => (
                  <div key={index} className="flex items-center gap-3 p-3 rounded-lg bg-white shadow-sm border border-slate-100">
                    <Avatar className="h-10 w-10">
                      <AvatarFallback className={`${getUserAvatarColor(user)}`}>
                        {user.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <p className="font-medium">{user}</p>
                      <p className="text-xs text-slate-500">
                        {user === username ? "(you)" : ""}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </SheetContent>
      </Sheet>
      
      {/* Desktop sidebar */}
      <aside className="hidden lg:flex flex-col w-72 border-r border-slate-200 bg-white">
        <div className="p-5 border-b border-slate-200">
          <h3 className="font-semibold text-lg flex items-center gap-2">
            <Users className="h-4 w-4" /> 
            Active Users ({users.length})
          </h3>
        </div>
        <div className="flex-1 overflow-y-auto p-4">
          <div className="space-y-3">
            {users.map((user, index) => (
              <div key={index} className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-50 transition-colors">
                <Avatar className="h-9 w-9">
                  <AvatarFallback className={`${getUserAvatarColor(user)} text-white`}>
                    {user.charAt(0).toUpperCase()}
                  </AvatarFallback>
                </Avatar>
                <div>
                  <p className="font-medium">{user}</p>
                  {user === username && (
                    <p className="text-xs text-slate-500">(you)</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="p-4 border-t border-slate-200">
          <div className="bg-slate-50 rounded-lg p-3 text-sm text-slate-700">
            <p className="font-medium mb-1">Session ID</p>
            <div className="flex items-center justify-between gap-2">
              <code className="text-xs bg-white px-2 py-1 rounded border overflow-hidden text-ellipsis">{sessionID}</code>
              <Button 
                variant="ghost" 
                size="icon"
                className="h-7 w-7" 
                onClick={copySessionId}
              >
                {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
              </Button>
            </div>
          </div>
        </div>
      </aside>

      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="border-b bg-white shadow-sm px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="icon" onClick={() => router.push('/')} className="rounded-full">
              <ArrowLeft className="h-5 w-5" />
            </Button>
            
            <Button 
              variant="ghost" 
              size="sm"
              className="lg:hidden flex items-center gap-1.5 rounded-full border border-slate-200"
              onClick={() => setShowUsersPanel(true)}
            >
              <Users className="h-4 w-4" />
              <span>{users.length}</span>
            </Button>
            
            <div>
              <h1 className="font-semibold text-lg">Multilingual Chat Room</h1>
              <p className="text-xs text-slate-500 hidden sm:block">
                Connected as <span className="font-medium text-slate-700">{username}</span>
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {/* Session ID (mobile only) */}
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="text-sm flex items-center gap-1.5 rounded-full lg:hidden"
                    onClick={copySessionId}
                  >
                    {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
                    <span className="hidden sm:inline">{copied ? "Copied" : "Copy ID"}</span>
                  </Button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Copy session ID: {sessionID.substring(0, 8)}...</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
            
            {/* Settings */}
            <Sheet>
              <SheetTrigger asChild>
                <Button variant="outline" size="icon" className="h-9 w-9 rounded-full">
                  <Settings className="h-4 w-4" />
                </Button>
              </SheetTrigger>
              <SheetContent className="bg-slate-50 p-4" >
                <SheetHeader>
                  <SheetTitle>Chat Settings</SheetTitle>
                  <SheetDescription>
                    Configure chat preferences and translation settings
                  </SheetDescription>
                </SheetHeader>
                <div className="py-6 space-y-5">
                  <div className="space-y-3">
                    <Label htmlFor="sutraApiKey">Sutra API Key</Label>
                    <Input
                      id="sutraApiKey"
                      type="password"
                      value={sutraApiKey}
                      onChange={(e) => {
                        setSutraApiKey(e.target.value)
                        localStorage.setItem("sutraApiKey", e.target.value)
                      }}
                      placeholder="Enter your Sutra API key for translations"
                      className="border-slate-200"
                    />
                    <p className="text-xs text-slate-500">
                      Required for translation features
                    </p>
                  </div>
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </header>

        {/* Language selector */}
        <div className="border-b bg-white px-4 py-2.5 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Globe className="h-4 w-4 text-indigo-500" />
            {/* Dropdown to select the display language for all messages */}
            <Select value={language} onValueChange={setLanguage}>
              <SelectTrigger className="bg-transparent border border-slate-200 rounded-full h-8 w-[180px] text-sm">
                <SelectValue placeholder="Select Language" />
              </SelectTrigger>
              <SelectContent>
                {/* List all supported languages - "original" is always first option */}
                {LANGUAGES.map((lang) => (
                  <SelectItem key={lang.code} value={lang.code}>
                    <div className="flex items-center gap-2">
                      {lang.flag && <span>{lang.flag}</span>}
                      <span>{lang.name}</span>
                    </div>
                  </SelectItem>
                ))}

                {/* Allow users to add custom language options if needed */}
                <div className="p-2 border-t flex flex-col gap-2 mt-1">
                  <p className="text-xs text-slate-500 font-medium">Add Custom Language</p>
                  <div className="flex gap-2">
                    <Input
                      placeholder="Language Name"
                      value={customLanguage}
                      onChange={(e) => setCustomLanguage(e.target.value)}
                      className="h-8 text-xs"
                    />
                    <Input
                      placeholder="Code (e.g. fr)"
                      value={customLanguageCode}
                      onChange={(e) => setCustomLanguageCode(e.target.value)}
                      className="h-8 text-xs w-20"
                    />
                  </div>
                  <Button 
                    size="sm" 
                    className="w-full h-8 mt-1" 
                    onClick={addCustomLanguage}
                    disabled={!customLanguage || !customLanguageCode}
                  >
                    Add
                  </Button>
                </div>
              </SelectContent>
            </Select>
            
            {/* Warning if translation is needed but no API key is provided */}
            {language !== "original" && !sutraApiKey && (
              <span className="text-xs text-red-500 hidden sm:inline-block">
                Set Sutra API key in settings
              </span>
            )}
          </div>
          
          {/* Translation in progress indicator */}
          {isTranslating && (
            <div className="flex items-center gap-1.5 text-xs font-medium text-indigo-600">
              <Loader2 className="h-3 w-3 animate-spin" />
              Translating...
            </div>
          )}
        </div>
        
        {/* Chat messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3" style={{ backgroundImage: 'radial-gradient(circle at 1rem 1rem, rgba(224, 231, 255, 0.15) 1rem, transparent 1rem)', backgroundSize: '3rem 3rem' }}>
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center p-6">
              <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
                <MessageSquare className="h-8 w-8 text-indigo-600" />
              </div>
              <h3 className="text-lg font-semibold text-slate-800">No messages yet</h3>
              <p className="text-slate-500 max-w-sm mt-1">
                Start the conversation by sending your first message below.
              </p>
            </div>
          ) : (
            messages.map((message, index) => {
              const isCurrentUser = message.username === username;
              const showAvatar = index === 0 || messages[index - 1].username !== message.username;
              
              return (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.2 }}
                  className={`flex gap-2 ${
                    isCurrentUser ? "justify-end" : "justify-start"
                  }`}
                >
                  {!isCurrentUser && showAvatar && (
                    <Avatar className="h-8 w-8 mt-1">
                      <AvatarFallback className={`${getUserAvatarColor(message.username)} text-white text-xs`}>
                        {message.username.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                  )}
                  
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-2.5 shadow-sm ${
                      isCurrentUser
                        ? "bg-gradient-to-br from-indigo-600 to-indigo-700 text-white"
                        : "bg-white border border-slate-200"
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      {!isCurrentUser && (
                        <span className="font-medium text-sm text-slate-700">
                          {message.username}
                        </span>
                      )}
                      <span className={`text-xs ${isCurrentUser ? "text-indigo-100" : "text-slate-400"}`}>
                        {formatTime(message.timestamp)}
                      </span>
                    </div>
                    <p className={`${language !== "original" && !translationCache[`${message.id}-${language}`] && "opacity-80"}`}>
                      {getMessageText(message)}
                    </p>
                  </div>
                  
                  {isCurrentUser && showAvatar && (
                    <Avatar className="h-8 w-8 mt-1">
                      <AvatarFallback className={`${getUserAvatarColor(message.username)} text-white text-xs`}>
                        {message.username.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                  )}
                </motion.div>
              );
            })
          )}
          <div ref={messagesEndRef} className="pt-2" />
        </div>

        {/* Message input */}
        <div className="border-t bg-white p-3 shadow-sm">
          <form
            onSubmit={(e) => {
              e.preventDefault()
              sendMessage()
            }}
            className="flex gap-2 items-center"
          >
            <Input
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Type a message..."
              className="flex-1 border-slate-200 bg-slate-50 focus-visible:bg-white transition-colors rounded-full py-5"
              disabled={sendingMessage}
            />
            <Button 
              type="submit" 
              disabled={!newMessage.trim() || sendingMessage}
              className="rounded-full bg-indigo-600 hover:bg-indigo-700"
            >
              {sendingMessage ? (
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Send className="h-4 w-4 mr-2" />
              )}
              Send
            </Button>
          </form>
          
          {/* Current language indicator (mobile) */}
          {language !== "original" && (
            <div className="mt-2 text-center lg:hidden">
              <p className="text-xs text-slate-500">
                Viewing messages in {getActiveLanguage().flag} {getActiveLanguage().name}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
