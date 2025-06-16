"use client"

import { useState, useEffect } from "react"
import { v4 as uuidv4 } from 'uuid'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Settings, MessageSquare, Users, ArrowRight, Globe, Sparkles } from "lucide-react"
import { Label } from "@/components/ui/label"
import { motion } from "framer-motion"

export default function Home() {
  const [username, setUsername] = useState("")
  const [sessionId, setSessionId] = useState("")
  const [sutraApiKey, setSutraApiKey] = useState("")
  const [createDialogOpen, setCreateDialogOpen] = useState(false)
  const [joinDialogOpen, setJoinDialogOpen] = useState(false)
  const [errorMsg, setErrorMsg] = useState("")
  const router = useRouter()

  // Load API key from localStorage on component mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedSutraKey = localStorage.getItem("sutraApiKey")
      if (savedSutraKey) setSutraApiKey(savedSutraKey)
    }
  }, [])

  // Save API key to localStorage when changed
  const saveSutraApiKey = (key: string) => {
    setSutraApiKey(key)
    if (typeof window !== "undefined") {
      localStorage.setItem("sutraApiKey", key)
    }
  }

  // Create a new chat room
  const createRoom = () => {
    if (!username.trim()) {
      setErrorMsg("Please enter a username")
      return
    }

    const newSessionId = uuidv4()
    router.push(`/chat/${newSessionId}?username=${encodeURIComponent(username)}`)
  }

  // Join an existing chat room
  const joinRoom = () => {
    if (!username.trim()) {
      setErrorMsg("Please enter a username")
      return
    }
    
    if (!sessionId.trim()) {
      setErrorMsg("Please enter a session ID")
      return
    }

    router.push(`/chat/${sessionId}?username=${encodeURIComponent(username)}`)
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-indigo-50 via-white to-blue-50">
      <div className="mx-auto px-4 sm:px-6 lg:px-8 max-w-6xl">
        {/* Header */}
        <header className="flex flex-col sm:flex-row justify-between items-center py-8">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-gradient-to-br from-indigo-600 to-blue-500 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-500/20 transition-transform hover:scale-105 rotate-3">
              <MessageSquare className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-indigo-600 to-blue-600 bg-clip-text text-transparent">
                Multilingual Chat
              </h1>
              <p className="text-slate-600 mt-1 max-w-md">
                Break language barriers and connect globally through real-time translated conversations
              </p>
            </div>
          </div>

          <div className="flex items-center mt-4 sm:mt-0">
            <div className="flex flex-wrap gap-3 items-center mr-3">
              {/* Status indicator for Sutra API key - shows green if key is present, red if missing */}
              <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full transition-all ${sutraApiKey ? "bg-green-50 text-green-700 border border-green-200" : "bg-red-50 text-red-600 border border-red-200"}`}>
                <span className={`inline-block w-2 h-2 ${sutraApiKey ? "bg-green-500" : "bg-red-500"} rounded-full`}></span>
                <span className="text-sm font-medium">Sutra API</span>
              </div>
            </div>

            {/* Settings dialog for configuring Sutra API key */}
            <Dialog>
              <DialogTrigger asChild>
                <Button 
                  id="settings-trigger" 
                  variant="outline" 
                  size="sm"
                  className="h-10 rounded-full border-slate-200 shadow-sm hover:shadow-md transition-all duration-200 hover:border-indigo-300"
                >
                  <Settings className="h-4 w-4 mr-1" />
                  <span className="hidden sm:inline">Settings</span>
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-md">
                <DialogHeader>
                  <DialogTitle className="text-xl">Translation Settings</DialogTitle>
                  <DialogDescription>
                    Enter your Sutra API key to enable real-time multilingual translations
                  </DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  {/* Sutra API key input field that saves to localStorage for persistence */}
                  <div className="grid gap-2">
                    <Label htmlFor="sutraApiKey" className="text-sm font-medium">
                      Sutra API Key
                    </Label>
                    <Input
                      id="sutraApiKey"
                      type="password"
                      value={sutraApiKey}
                      onChange={(e) => saveSutraApiKey(e.target.value)}
                      className="border-slate-200"
                      placeholder="Enter your API key"
                    />
                    <p className="text-xs text-slate-500">
                      Required for translation features.{" "}
                      <a
                        href="https://www.two.ai/sutra/api"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-indigo-600 hover:text-indigo-500 hover:underline font-medium"
                      >
                        Get your Sutra API key
                      </a>
                    </p>
                  </div>
                </div>
              </DialogContent>
            </Dialog>
          </div>
        </header>

        {/* Hero Section */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center py-12 md:py-20"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-slate-800 max-w-3xl mx-auto leading-tight">
            Chat with anyone, <span className="text-indigo-600">in any language</span>
          </h2>
          <p className="mt-5 text-xl text-slate-600 max-w-2xl mx-auto">
            Real-time translation across multiple languages, powered by Sutra AI
          </p>
          <div className="flex flex-wrap justify-center gap-3 mt-8">
            <span className="px-4 py-2 bg-white rounded-full text-sm font-medium shadow-sm border border-slate-200 flex items-center">
              <Globe className="h-4 w-4 mr-2 text-indigo-500" /> 10+ Languages
            </span>
            <span className="px-4 py-2 bg-white rounded-full text-sm font-medium shadow-sm border border-slate-200 flex items-center">
              <Sparkles className="h-4 w-4 mr-2 text-indigo-500" /> AI Translation
            </span>
            <span className="px-4 py-2 bg-white rounded-full text-sm font-medium shadow-sm border border-slate-200 flex items-center">
              <Users className="h-4 w-4 mr-2 text-indigo-500" /> Group Chats
            </span>
          </div>
        </motion.div>

        {/* Action Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 pb-20">
          {/* Create Room Card */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card className="overflow-hidden border-0 shadow-xl shadow-indigo-100/40 hover:shadow-2xl hover:shadow-indigo-200/50 transition-all duration-300 h-full">
              {/* <div className="absolute inset-0 bg-gradient-to-br from-indigo-50 to-indigo-100 opacity-50 z-0"></div> */}
              <CardHeader className="pb-4 relative z-10">
                <CardTitle className="text-2xl md:text-3xl font-bold text-indigo-900">Create a Room</CardTitle>
                <CardDescription className="text-indigo-700">Start a new chat room and invite others</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6 relative z-10 pb-8">
                <div className="flex justify-center py-8">
                  <div className="w-24 h-24 bg-gradient-to-br from-indigo-100 to-indigo-50 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-200/30 rotate-3 border border-indigo-200/50">
                    <Users className="h-12 w-12 text-indigo-600" />
                  </div>
                </div>
                <Button 
                  className="w-full h-14 text-lg font-medium rounded-xl bg-indigo-600 hover:bg-indigo-700 transition-all"
                  onClick={() => setCreateDialogOpen(true)}
                >
                  Create New Room
                  <ArrowRight className="h-5 w-5 ml-2" />
                </Button>
              </CardContent>
            </Card>
          </motion.div>

          {/* Join Room Card */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Card className="overflow-hidden border-0 shadow-xl shadow-blue-100/40 hover:shadow-2xl hover:shadow-blue-200/50 transition-all duration-300 h-full">
              {/* <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-blue-100 opacity-50 z-0"></div> */}
              <CardHeader className="pb-4 relative z-10">
                <CardTitle className="text-2xl md:text-3xl font-bold text-blue-900">Join a Room</CardTitle>
                <CardDescription className="text-blue-700">Enter a session ID to join an existing chat</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6 relative z-10 pb-8">
                <div className="flex justify-center py-8">
                  <div className="w-24 h-24 bg-gradient-to-br from-blue-100 to-blue-50 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-200/30 -rotate-3 border border-blue-200/50">
                    <MessageSquare className="h-12 w-12 text-blue-600" />
                  </div>
                </div>
                <Button 
                  className="w-full h-14 text-lg font-medium rounded-xl bg-blue-600 hover:bg-blue-700 transition-all"
                  onClick={() => setJoinDialogOpen(true)}
                >
                  Join Existing Room
                  <ArrowRight className="h-5 w-5 ml-2" />
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Create Room Dialog */}
        <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle className="text-2xl font-bold text-indigo-900">Create a New Chat Room</DialogTitle>
              <DialogDescription className="text-indigo-700">
                Enter your name to create and join a multilingual chat room
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-5 py-6">
              <div className="space-y-3">
                <Label htmlFor="create-username" className="text-sm font-medium">Your Name</Label>
                <Input 
                  id="create-username" 
                  placeholder="Enter your display name" 
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="h-12 border-slate-200"
                />
              </div>
              {errorMsg && (
                <div className="p-3 bg-red-50 border border-red-100 rounded-lg text-sm text-red-600">
                  {errorMsg}
                </div>
              )}
              <Button 
                className="w-full h-12 text-lg font-medium rounded-xl bg-indigo-600 hover:bg-indigo-700 transition-all"
                onClick={createRoom}
              >
                Create & Join Room
                <ArrowRight className="h-5 w-5 ml-2" />
              </Button>
            </div>
          </DialogContent>
        </Dialog>

        {/* Join Room Dialog */}
        <Dialog open={joinDialogOpen} onOpenChange={setJoinDialogOpen}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle className="text-2xl font-bold text-blue-900">Join a Chat Room</DialogTitle>
              <DialogDescription className="text-blue-700">
                Enter your details to join an existing multilingual chat room
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-5 py-6">
              <div className="space-y-3">
                <Label htmlFor="join-username" className="text-sm font-medium">Your Name</Label>
                <Input 
                  id="join-username" 
                  placeholder="Enter your display name" 
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="h-12 border-slate-200"
                />
              </div>
              <div className="space-y-3">
                <Label htmlFor="session-id" className="text-sm font-medium">Session ID</Label>
                <Input 
                  id="session-id" 
                  placeholder="Enter the room's session ID" 
                  value={sessionId}
                  onChange={(e) => setSessionId(e.target.value)}
                  className="h-12 border-slate-200"
                />
              </div>
              {errorMsg && (
                <div className="p-3 bg-red-50 border border-red-100 rounded-lg text-sm text-red-600">
                  {errorMsg}
                </div>
              )}
              <Button 
                className="w-full h-12 text-lg font-medium rounded-xl bg-blue-600 hover:bg-blue-700 transition-all"
                onClick={joinRoom}
              >
                Join Chat Room
                <ArrowRight className="h-5 w-5 ml-2" />
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </main>
  )
}
