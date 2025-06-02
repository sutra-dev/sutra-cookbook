"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { AlertCircle, Settings, Video, Download, ArrowRight, Loader2, Copy, CheckCircle, Clock, Eye, ThumbsUp, X, HelpCircle } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

export default function Home() {
  // State variables
  const [youtubeUrl, setYoutubeUrl] = useState("")
  const [originalTranscript, setOriginalTranscript] = useState("")
  const [translatedTranscript, setTranslatedTranscript] = useState("")
  const [translationError, setTranslationError] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [includeTimestamps, setIncludeTimestamps] = useState(true)
  const [formatTranscript, setFormatTranscript] = useState(true)
  const [includeVideoInfo, setIncludeVideoInfo] = useState(false)
  const [error, setError] = useState("")
  const [activeTab, setActiveTab] = useState("input")
  const [rapidApiKey, setRapidApiKey] = useState("")
  const [sutraApiKey, setSutraApiKey] = useState("")
  const [videoInfo, setVideoInfo] = useState<any>(null)
  const [copied, setCopied] = useState<'original' | 'translated' | null>(null)
  const [targetLanguage, setTargetLanguage] = useState("")
  const [customLanguage, setCustomLanguage] = useState("")

  // Languages supported by Sutra
  const LANGUAGES = [
    // Indian Languages
    { name: "Hindi", code: "hi", flag: "🇮🇳" },
    { name: "Tamil", code: "ta", flag: "🇮🇳" },
    { name: "Telugu", code: "te", flag: "🇮🇳" },
    { name: "Bengali", code: "bn", flag: "🇮🇳" },
    { name: "Marathi", code: "mr", flag: "🇮🇳" },
    { name: "Punjabi", code: "pa", flag: "🇮🇳" },
    { name: "Malayalam", code: "ml", flag: "🇮🇳" },
    { name: "Kannada", code: "kn", flag: "🇮🇳" },
    { name: "Gujarati", code: "gu", flag: "🇮🇳" },
    { name: "Odia", code: "or", flag: "🇮🇳" },
    { name: "Assamese", code: "as", flag: "🇮🇳" },
    { name: "Kashmiri", code: "ks", flag: "🇮🇳" },
    { name: "Konkani", code: "kok", flag: "🇮🇳" },
    { name: "Manipuri", code: "mni", flag: "🇮🇳" },
    { name: "Nepali", code: "ne", flag: "🇮🇳" },
    { name: "Sanskrit", code: "sa", flag: "🇮🇳" },
    { name: "Sindhi", code: "sd", flag: "🇮🇳" },
    { name: "Urdu", code: "ur", flag: "🇮🇳" },
    // International Languages
    { name: "English", code: "en", flag: "🇬🇧" },
    { name: "French", code: "fr", flag: "🇫🇷" },
    { name: "German", code: "de", flag: "🇩🇪" },
    { name: "Spanish", code: "es", flag: "🇪🇸" },
    { name: "Japanese", code: "ja", flag: "🇯🇵" },
    { name: "Chinese", code: "zh", flag: "🇨🇳" },
    { name: "Russian", code: "ru", flag: "🇷🇺" },
    { name: "Arabic", code: "ar", flag: "🇸🇦" },
    { name: "Portuguese", code: "pt", flag: "🇵🇹" },
    { name: "Korean", code: "ko", flag: "🇰🇷" },
    { name: "Italian", code: "it", flag: "🇮🇹" },
  ]

  // Load API keys from localStorage on component mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedRapidAPIKey = localStorage.getItem("rapidApiKey")
      const savedSutraKey = localStorage.getItem("sutraApiKey")
      if (savedRapidAPIKey) setRapidApiKey(savedRapidAPIKey)
      if (savedSutraKey) setSutraApiKey(savedSutraKey)
    }
  }, [])

  // Save API keys to localStorage when they change
  useEffect(() => {
    if (typeof window !== "undefined") {
      if (rapidApiKey) localStorage.setItem("rapidApiKey", rapidApiKey)
      if (sutraApiKey) localStorage.setItem("sutraApiKey", sutraApiKey)
    }
  }, [rapidApiKey, sutraApiKey])

  // Clear API keys
  const clearApiKey = (type: 'rapid' | 'sutra') => {
    if (type === 'rapid') {
      setRapidApiKey("")
      localStorage.removeItem("rapidApiKey")
    } else {
      setSutraApiKey("")
      localStorage.removeItem("sutraApiKey")
    }
  }

  // Sample YouTube URLs for testing
  const SAMPLE_URLS = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://youtu.be/x--N03NO130?si=DZXL5MdbMisb5HNe",
    "https://youtu.be/jTiHNHa9er8?si=2g_4URpwM47YufMk",
    "https://youtu.be/c_eKp1E48DE?si=6GUNxQaC78PgDUXZ",
  ]



  // Validate YouTube URL
  const isValidYouTubeUrl = (url: string) => {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|embed\/)|youtu\.be\/)[\w-]+/
    return youtubeRegex.test(url)
  }

  // Extract video ID from YouTube URL
  const extractVideoId = (url: string) => {
    const regex = /(?:youtube\.com\/(?:[^/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?/\s]{11})/
    const match = url.match(regex)
    return match ? match[1] : null
  }

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Validate inputs
    if (!youtubeUrl.trim()) {
      setError("Please enter a valid YouTube URL.")
      return
    }

    if (!isValidYouTubeUrl(youtubeUrl)) {
      setError("Please enter a valid YouTube URL.")
      return
    }

    if (!rapidApiKey) {
      setError("Please set your RapidAPI key in settings.")
      return
    }

    if (targetLanguage && !sutraApiKey) {
      setError("Please set your Sutra API key in settings to use translation features.")
      return
    }

    setIsLoading(true)
    setError("")
    setOriginalTranscript("")
    setTranslatedTranscript("")
    setTranslationError("")
    setVideoInfo(null)
    setActiveTab("results")

    try {
      const result = await generateTranscript(youtubeUrl)
      if (result.success) {
        setOriginalTranscript(result.originalTranscript)
        setTranslatedTranscript(result.translatedTranscript)
        setTranslationError(result.translationError)
        setVideoInfo(result.videoInfo)
      } else {
        throw new Error(result.error)
      }
    } catch (err: any) {
      setError(err.message || "Failed to generate transcript. Please try again.")
      setActiveTab("input")
    } finally {
      setIsLoading(false)
    }
  }

  // Generate transcript using APIs
  const generateTranscript = async (url: string) => {
    const response = await fetch("/api/transcript", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        youtubeUrl: url,
        includeTimestamps,
        formatTranscript,
        rapidApiKey,
        sutraApiKey: targetLanguage ? sutraApiKey : undefined,
        targetLanguage,
        includeVideoInfo,
      }),
    })

    const data = await response.json()
    if (!response.ok) {
      throw new Error(data.error || "Failed to generate transcript")
    }

    return data
  }

  // Reset form
  const resetForm = () => {
    setYoutubeUrl("")
    setOriginalTranscript("")
    setTranslatedTranscript("")
    setVideoInfo(null)
    setError("")
    setActiveTab("input")
  }

  // Set sample URL
  const setSampleUrl = (url: string) => {
    setYoutubeUrl(url)
  }

  // Copy transcript to clipboard
  const copyToClipboard = async (text: string, type: 'original' | 'translated') => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(type)
      setTimeout(() => setCopied(null), 2000)
    } catch (err) {
      console.error("Failed to copy text: ", err)
    }
  }

  // Download transcript as text file
  const downloadTranscript = (text: string, type: 'original' | 'translated') => {
    const element = document.createElement("a")
    const file = new Blob([text], { type: "text/plain" })
    element.href = URL.createObjectURL(file)
    const langSuffix = type === 'translated' ? `-${targetLanguage.toLowerCase()}` : ''
    element.download = `transcript${langSuffix}-${videoInfo?.title?.replace(/[^a-z0-9]/gi, "_").toLowerCase() || "video"}.txt`
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="container mx-auto p-4 max-w-7xl">
        <header className="flex justify-between items-center py-8 mb-8">
          <div className="flex items-center space-x-6">
            <div className="w-12 h-12 bg-gradient-to-br from-red-500 to-red-600 rounded-xl flex items-center justify-center shadow-lg shadow-red-500/20 transition-transform hover:scale-105">
              <Video className="h-7 w-7 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
                Multilingual YouTube Transcript Generator
              </h1>
              <p className="text-slate-600 mt-1">Generate and translate YouTube transcripts with ease</p>
              <div className="flex flex-wrap gap-4 text-xs text-slate-500 mt-2 items-center">
                <div className="flex items-center gap-1.5 bg-white px-2 py-1 rounded-full shadow-sm">
                  <span className={`inline-block w-2 h-2 ${rapidApiKey ? "bg-green-500" : "bg-red-500"} rounded-full`}></span>
                  <span>RapidAPI</span>
                </div>
                <div className="flex items-center gap-1.5 bg-white px-2 py-1 rounded-full shadow-sm">
                  <span className={`inline-block w-2 h-2 ${sutraApiKey ? "bg-green-500" : "bg-red-500"} rounded-full`}></span>
                  <span>Sutra API</span>
                </div>
                {(!rapidApiKey || !sutraApiKey) && (
                  <Button
                    variant="link"
                    size="sm"
                    className="text-xs p-0 h-auto text-blue-600 font-medium"
                    onClick={() => document.getElementById("settings-trigger")?.click()}
                  >
                    Set API Keys
                  </Button>
                )}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Dialog>
              <DialogTrigger asChild>
                <Button
                  variant="outline"
                  size="icon"
                  className="h-10 w-10 rounded-xl shadow-sm hover:shadow-md transition-all duration-200"
                >
                  <HelpCircle className="h-4 w-4" />
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[600px] max-h-[80vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle className="text-2xl mb-4">How to Use This App</DialogTitle>
                </DialogHeader>
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-semibold mb-2 text-slate-900">1. Set Up API Keys</h3>
                    <div className="space-y-3 text-slate-600">
                      <div className="space-y-4">
                        <div className="text-sm space-y-2">
                          <div className="font-medium text-slate-800">Step 1: Get RapidAPI Key</div>
                          <ol className="list-decimal ml-4 space-y-2">
                            <li>Visit <a href="https://rapidapi.com/hub" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline font-medium">RapidAPI</a></li>
                            <li>Sign up or log in to your account</li>
                            <li>Go to your dashboard</li>
                            <li>Find your API key under "Security" or "API Key"</li>
                          </ol>
                        </div>

                        <div className="text-sm space-y-2">
                          <div className="font-medium text-slate-800">Step 2: Subscribe to YouTube Transcript API (Required)</div>
                          <ol className="list-decimal ml-4 space-y-2">
                            <li>Visit the <a href="https://rapidapi.com/solid-api-solid-api-default/api/youtube-transcript3" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline font-medium">YouTube Transcript API</a></li>
                            <li>Click "Subscribe to Test"</li>
                            <li>Choose a subscription plan (Basic plan is free)</li>
                            <li>Complete the subscription process</li>
                          </ol>
                        </div>

                        <div className="text-sm space-y-2">
                          <div className="font-medium text-slate-800">Step 3: Subscribe to Video Information API (Optional)</div>
                          <ol className="list-decimal ml-4 space-y-2">
                            <li>Visit the <a href="https://rapidapi.com/metekuscu/api/youtube-video-information1" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline font-medium">Video Information API</a></li>
                            <li>Click "Subscribe to Test"</li>
                            <li>Choose a subscription plan (Basic plan is free)</li>
                            <li>Complete the subscription process</li>
                          </ol>
                          <div className="text-xs text-slate-500 mt-1">
                            Note: This API is only needed if you want to display video metadata (title, views, etc.)
                          </div>
                        </div>

                        <div className="text-sm space-y-2">
                          <div className="font-medium text-slate-800">Step 4: Get Sutra API Key (Optional - For Translation)</div>
                          <ol className="list-decimal ml-4 space-y-2">
                            <li>Visit <a href="https://www.two.ai/sutra/api" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline font-medium">Sutra API</a></li>
                            <li>Sign up for an account</li>
                            <li>Navigate to API section</li>
                            <li>Generate or copy your API key</li>
                          </ol>
                          <div className="text-xs text-slate-500 mt-1">
                            Note: Only required if you want to translate transcripts
                          </div>
                        </div>

                        <Alert className="bg-blue-50 text-blue-800 border-blue-200">
                          <AlertCircle className="h-4 w-4 text-blue-500" />
                          <AlertTitle>Subscription Tips</AlertTitle>
                          <AlertDescription className="text-blue-700">
                            <ul className="list-disc ml-4 space-y-1 mt-1">
                              <li>Free tiers are available for all required APIs</li>
                              <li>RapidAPI subscriptions renew monthly</li>
                              <li>Monitor your API usage in RapidAPI dashboard</li>
                              <li>Keep your API keys secure and never share them</li>
                            </ul>
                          </AlertDescription>
                        </Alert>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold mb-2 text-slate-900">2. Configure Settings</h3>
                    <div className="space-y-2 text-sm text-slate-600">
                      <div>Click the settings icon (⚙️) to:</div>
                      <ul className="list-disc ml-6 space-y-1">
                        <li>Enter your API keys in the respective fields</li>
                        <li>Toggle timestamp inclusion in transcripts</li>
                        <li>Toggle video information display</li>
                        <li>Save settings (automatically saved)</li>
                      </ul>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold mb-2 text-slate-900">3. Generate Transcript</h3>
                    <div className="space-y-2 text-sm text-slate-600">
                      <div>a. Paste a YouTube URL in the input field</div>
                      <div>b. (Optional) Select a target language for translation</div>
                      <div>c. Click "Generate Transcript"</div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold mb-2 text-slate-900">4. Working with Results</h3>
                    <div className="space-y-2 text-sm text-slate-600">
                      <div>You can:</div>
                      <ul className="list-disc ml-6 space-y-1">
                        <li>View the original transcript</li>
                        <li>View the translated version (if language selected)</li>
                        <li>Copy transcripts to clipboard</li>
                        <li>Download transcripts as text files</li>
                        <li>View video information (if enabled)</li>
                      </ul>
                    </div>
                  </div>

                  <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertTitle>Important</AlertTitle>
                    <AlertDescription>
                      <div className="space-y-2">
                        <div>Before using the app, ensure you have:</div>
                        <ul className="list-disc ml-4 space-y-1">
                          <li>Active RapidAPI subscription for YouTube Transcript API</li>
                          <li>Video Information API subscription (if needed)</li>
                          <li>Valid API keys entered in settings</li>
                        </ul>
                      </div>
                    </AlertDescription>
                  </Alert>
                </div>
              </DialogContent>
            </Dialog>

            <Sheet>
              <SheetTrigger asChild>
                <Button 
                  id="settings-trigger" 
                  variant="outline" 
                  size="icon"
                  className="h-10 w-10 rounded-xl shadow-sm hover:shadow-md transition-all duration-200"
                >
                  <Settings className="h-4 w-4" />
                </Button>
              </SheetTrigger>
              <SheetContent className="sm:max-w-[425px] p-4">
                <SheetHeader className="mb-6">
                  <SheetTitle className="text-2xl">Settings</SheetTitle>
                  <SheetDescription>Configure your API keys and preferences</SheetDescription>
                </SheetHeader>
                <div className="space-y-6">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="includeTimestamps" className="font-medium">Include timestamps</Label>
                      <Switch
                        id="includeTimestamps"
                        checked={includeTimestamps}
                        onCheckedChange={setIncludeTimestamps}
                      />
                    </div>
                    <p className="text-sm text-slate-500">
                      Add timestamps to the transcript for better navigation
                    </p>
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="includeVideoInfo" className="font-medium">Include video information</Label>
                      <Switch
                        id="includeVideoInfo"
                        checked={includeVideoInfo}
                        onCheckedChange={setIncludeVideoInfo}
                      />
                    </div>
                    <p className="text-sm text-slate-500">
                      Show video thumbnail, title, views, and other metadata
                    </p>
                  </div>

                  <Separator className="my-6" />

                  <div className="space-y-4">
                    <h3 className="text-sm font-semibold">API Configuration</h3>
                    
                    {/* RapidAPI Key Section */}
                    <div className="space-y-2 p-4 bg-white rounded-xl border shadow-sm">
                      <div className="flex items-center gap-2">
                        <Label htmlFor="rapidApiKey" className="font-medium">RapidAPI Key</Label>
                        {rapidApiKey && (
                          <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                            Set
                          </Badge>
                        )}
                      </div>
                      <div className="flex gap-2">
                        <input
                          id="rapidApiKey"
                          type="password"
                          className="flex-1 px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                          value={rapidApiKey}
                          onChange={(e) => setRapidApiKey(e.target.value)}
                          placeholder="Enter your RapidAPI key"
                        />
                        {rapidApiKey && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => clearApiKey('rapid')}
                            className="shrink-0"
                          >
                            Clear
                          </Button>
                        )}
                      </div>
                      <p className="text-xs text-slate-500">
                        Required for YouTube transcript generation.{" "}
                        <a
                          href="https://rapidapi.com/hub"
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:underline font-medium"
                        >
                          Get your RapidAPI key
                        </a>
                        <br />
                        Subscribe to required APIs:{" "}
                        <a
                          href="https://rapidapi.com/solid-api-solid-api-default/api/youtube-transcript3"
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:underline font-medium"
                        >
                          YouTube Transcript API
                        </a>
                        {includeVideoInfo && (
                          <>
                            {" "}and{" "}
                            <a
                              href="https://rapidapi.com/metekuscu/api/youtube-video-information1"
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-600 hover:underline font-medium"
                            >
                              Video Information API
                            </a>
                          </>
                        )}
                      </p>
                    </div>

                    {/* Sutra API Key Section */}
                    <div className="space-y-2 p-4 bg-white rounded-xl border shadow-sm">
                      <div className="flex items-center gap-2">
                        <Label htmlFor="sutraApiKey" className="font-medium">Sutra API Key</Label>
                        {sutraApiKey && (
                          <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                            Set
                          </Badge>
                        )}
                      </div>
                      <div className="flex gap-2">
                        <input
                          id="sutraApiKey"
                          type="password"
                          className="flex-1 px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                          value={sutraApiKey}
                          onChange={(e) => setSutraApiKey(e.target.value)}
                          placeholder="Enter your Sutra API key"
                        />
                        {sutraApiKey && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => clearApiKey('sutra')}
                            className="shrink-0"
                          >
                            Clear
                          </Button>
                        )}
                      </div>
                      <p className="text-xs text-slate-500">
                        Required for translation features.{" "}
                        <a
                          href="https://www.two.ai/sutra/api"
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:underline font-medium"
                        >
                          Get your Sutra API key
                        </a>
                      </p>
                    </div>
                  </div>
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </header>

        <Tabs 
          value={activeTab} 
          onValueChange={setActiveTab} 
          className="space-y-6"
        >
          <TabsList className="grid w-full grid-cols-2 h-12 items-center bg-white shadow-sm rounded-xl p-1">
            <TabsTrigger 
              value="input"
              className="rounded-lg data-[state=active]:bg-slate-100 data-[state=active]:shadow-sm transition-all duration-200"
            >
              Input
            </TabsTrigger>
            <TabsTrigger 
              value="results"
              className="rounded-lg data-[state=active]:bg-slate-100 data-[state=active]:shadow-sm transition-all duration-200"
            >
              Results
            </TabsTrigger>
          </TabsList>

          <TabsContent value="input">
            <Card className="border-0 shadow-lg shadow-slate-200/50">
              <CardHeader className="space-y-1">
                <CardTitle className="text-2xl">Generate YouTube Transcript</CardTitle>
                <CardDescription className="text-slate-500">
                  Enter a YouTube URL to generate an accurate transcript using AI
                </CardDescription>
              </CardHeader>
              <CardContent>
                {error && (
                  <Alert variant="destructive" className="mb-6">
                    <AlertCircle className="h-4 w-4" />
                    <AlertTitle>Error</AlertTitle>
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}

                {!rapidApiKey && (
                  <Alert className="mb-6 border-blue-100 bg-blue-50">
                    <AlertCircle className="h-4 w-4 text-blue-600" />
                    <AlertTitle className="text-blue-800 font-medium">RapidAPI Key Required</AlertTitle>
                    <AlertDescription className="text-blue-700">
                      Please set your RapidAPI key in the settings to use the application.{" "}
                      <a
                        href="https://rapidapi.com/hub"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-800 font-medium hover:underline"
                      >
                        Get your API key
                      </a>
                    </AlertDescription>
                  </Alert>
                )}

                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="space-y-2">
                    <Label htmlFor="youtubeUrl" className="text-sm font-medium">YouTube URL</Label>
                    <Input
                      id="youtubeUrl"
                      placeholder="https://www.youtube.com/watch?v=..."
                      value={youtubeUrl}
                      onChange={(e) => setYoutubeUrl(e.target.value)}
                      className="h-12 px-4 shadow-sm"
                    />
                    <p className="text-xs text-slate-500">Supports youtube.com and youtu.be URLs</p>
                  </div>

                  <div className="space-y-3">
                    <Label className="text-sm font-medium">Target Language (Optional)</Label>
                    <div className="space-y-4">
                      <div className="flex flex-wrap gap-2">
                        {LANGUAGES.map((lang) => (
                          <Badge
                            key={lang.code}
                            variant={targetLanguage === lang.name ? "default" : "outline"}
                            className={`cursor-pointer px-3 py-1 text-sm transition-all duration-200 ${
                              targetLanguage === lang.name 
                                ? "bg-blue-100 text-blue-700 hover:bg-blue-200" 
                                : "hover:bg-slate-100"
                            }`}
                            onClick={() => {
                              setTargetLanguage(targetLanguage === lang.name ? "" : lang.name);
                              setCustomLanguage("");
                            }}
                          >
                            {lang.flag} {lang.name}
                          </Badge>
                        ))}
                      </div>
                      <div className="flex gap-2">
                        <Input
                          placeholder="Enter custom language..."
                          value={customLanguage}
                          onChange={(e) => {
                            setCustomLanguage(e.target.value);
                            if (e.target.value) {
                              setTargetLanguage(e.target.value);
                            }
                          }}
                          className="max-w-xs"
                        />
                        {customLanguage && (
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => {
                              setCustomLanguage("");
                              setTargetLanguage("");
                            }}
                            className="h-10 w-10"
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        )}
                      </div>
                    </div>
                  </div>

                  <Button 
                    type="submit" 
                    className="w-full h-12 text-base font-medium shadow-lg shadow-blue-500/25 transition-all duration-200 hover:shadow-xl hover:shadow-blue-500/20" 
                    disabled={isLoading || !rapidApiKey}
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-2 h-5 w-5 animate-spin" /> 
                        Generating Transcript...
                      </>
                    ) : (
                      <>
                        Generate Transcript 
                        <ArrowRight className="ml-2 h-5 w-5" />
                      </>
                    )}
                  </Button>
                </form>
              </CardContent>

              <CardFooter className="flex-col items-start space-y-6 bg-slate-50/50 rounded-b-lg border-t">
                <div className="w-full">
                  <h3 className="text-sm font-medium mb-3">Sample YouTube URLs</h3>
                  <div className="grid gap-2">
                    {SAMPLE_URLS.map((url, index) => (
                      <Button
                        key={index}
                        variant="outline"
                        className="w-full justify-start text-left text-sm h-auto py-2 px-4 bg-white hover:bg-slate-50 transition-colors duration-200"
                        onClick={() => setSampleUrl(url)}
                      >
                        {url}
                      </Button>
                    ))}
                  </div>
                </div>

              </CardFooter>
            </Card>
          </TabsContent>

          <TabsContent value="results">
            <Card className="border-0 shadow-lg shadow-slate-200/50">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-2xl">
                      {originalTranscript ? "📝 Generated Transcript" : "No Transcript Yet"}
                    </CardTitle>
                    <CardDescription className="text-slate-500">
                      {originalTranscript
                        ? "Your YouTube video transcript is ready"
                        : "Submit a YouTube URL to generate a transcript"}
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>

              <CardContent>
                {isLoading ? (
                  <div className="flex items-center justify-center p-16">
                    <div className="text-center">
                      <Loader2 className="h-12 w-12 animate-spin text-blue-500 mx-auto mb-4" />
                      <p className="text-slate-500">
                        {targetLanguage 
                          ? "Processing video, generating transcript and translating..." 
                          : "Processing video and generating transcript..."}
                      </p>
                    </div>
                  </div>
                ) : originalTranscript ? (
                  <>
                    {videoInfo && includeVideoInfo && (
                      <div className="mb-6 p-4 bg-white rounded-xl border shadow-sm">
                        <div className="flex gap-6">
                          {videoInfo.thumbnail && (
                            <div className="flex-shrink-0">
                              <img
                                src={videoInfo.thumbnail}
                                alt={videoInfo.title}
                                className="w-48 h-27 object-cover rounded-lg shadow-sm"
                              />
                            </div>
                          )}
                          <div className="flex-grow space-y-3">
                            <h4 className="font-medium text-lg text-slate-900">{videoInfo.title}</h4>
                            <div className="text-sm text-slate-500 space-y-2">
                              <div className="flex items-center gap-6">
                                <span className="flex items-center gap-1.5">
                                  <Clock className="h-4 w-4" />
                                  {videoInfo.duration}
                                </span>
                                <span className="flex items-center gap-1.5">
                                  <Eye className="h-4 w-4" />
                                  {videoInfo.views} views
                                </span>
                                <span className="flex items-center gap-1.5">
                                  <ThumbsUp className="h-4 w-4" />
                                  {videoInfo.likes} likes
                                </span>
                              </div>
                              <p className="text-sm">
                                Published on {videoInfo.publishedAt}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {/* Original Transcript */}
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <h3 className="text-lg font-medium text-slate-900">Original Transcript</h3>
                          <div className="flex gap-2">
                            <Button 
                              variant="outline" 
                              size="sm" 
                              onClick={() => copyToClipboard(originalTranscript, 'original')} 
                              className="flex items-center gap-2 h-9"
                            >
                              {copied === 'original' ? (
                                <>
                                  <CheckCircle className="h-4 w-4 text-green-500" />
                                  <span className="text-green-600">Copied!</span>
                                </>
                              ) : (
                                <>
                                  <Copy className="h-4 w-4" />
                                  Copy
                                </>
                              )}
                            </Button>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => downloadTranscript(originalTranscript, 'original')}
                              className="flex items-center gap-2 h-9"
                            >
                              <Download className="h-4 w-4" />
                              Download
                            </Button>
                          </div>
                        </div>
                        <div className="prose prose-slate max-w-none">
                          <Textarea 
                            value={originalTranscript} 
                            readOnly 
                            className="min-h-[400px] font-mono text-sm shadow-sm focus:border-blue-500 focus:ring-blue-500" 
                          />
                        </div>
                      </div>

                      {/* Translated Transcript */}
                      {targetLanguage && (
                        <div className="space-y-4">
                          <div className="flex items-center justify-between">
                            <h3 className="text-lg font-medium text-slate-900">
                              {targetLanguage} Translation
                              {translationError && (
                                <Badge variant="destructive" className="ml-2">
                                  Translation Failed
                                </Badge>
                              )}
                            </h3>
                            {!translationError && (
                              <div className="flex gap-2">
                                <Button 
                                  variant="outline" 
                                  size="sm" 
                                  onClick={() => copyToClipboard(translatedTranscript, 'translated')} 
                                  className="flex items-center gap-2 h-9"
                                >
                                  {copied === 'translated' ? (
                                    <>
                                      <CheckCircle className="h-4 w-4 text-green-500" />
                                      <span className="text-green-600">Copied!</span>
                                    </>
                                  ) : (
                                    <>
                                      <Copy className="h-4 w-4" />
                                      Copy
                                    </>
                                  )}
                                </Button>
                                <Button
                                  variant="outline"
                                  size="sm"
                                  onClick={() => downloadTranscript(translatedTranscript, 'translated')}
                                  className="flex items-center gap-2 h-9"
                                >
                                  <Download className="h-4 w-4" />
                                  Download
                                </Button>
                              </div>
                            )}
                          </div>
                          <div className="prose prose-slate max-w-none">
                            {translationError ? (
                              <Alert variant="destructive">
                                <AlertCircle className="h-4 w-4" />
                                <AlertTitle>Translation Error</AlertTitle>
                                <AlertDescription>{translationError}</AlertDescription>
                              </Alert>
                            ) : (
                              <Textarea 
                                value={translatedTranscript} 
                                readOnly 
                                className="min-h-[400px] font-mono text-sm shadow-sm focus:border-blue-500 focus:ring-blue-500" 
                              />
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </>
                ) : (
                  <div className="text-center p-16">
                    <Video className="h-16 w-16 mx-auto mb-4 text-slate-200" />
                    <p className="text-slate-500">No transcript to display yet. Please submit a YouTube URL.</p>
                  </div>
                )}
              </CardContent>

              {originalTranscript && (
                <CardFooter className="border-t py-6">
                  <Button 
                    onClick={resetForm} 
                    variant="outline"
                    className="h-11 px-6 text-base shadow-sm hover:shadow-md transition-all duration-200"
                  >
                    New Video
                  </Button>
                </CardFooter>
              )}
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
