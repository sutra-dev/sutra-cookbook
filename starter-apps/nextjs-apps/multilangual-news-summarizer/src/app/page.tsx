"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import Image from "next/image";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle, Settings, Languages, Newspaper, ArrowRight, Loader2 } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";

export default function Home() {
  // State variables
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [useSearch, setUseSearch] = useState(true);
  const [showToolCalls, setShowToolCalls] = useState(true);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("query");
  const [sutraApiKey, setSutraApiKey] = useState("");
  const [serpApiKey, setSerpApiKey] = useState("");

  // Load API keys from localStorage on component mount
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const savedSutraKey = localStorage.getItem('sutraApiKey');
      const savedSerpKey = localStorage.getItem('serpApiKey');
      
      if (savedSutraKey) setSutraApiKey(savedSutraKey);
      if (savedSerpKey) setSerpApiKey(savedSerpKey);
    }
  }, []);
  
  // Save API keys to localStorage when they change
  useEffect(() => {
    if (typeof window !== 'undefined' && sutraApiKey) {
      localStorage.setItem('sutraApiKey', sutraApiKey);
    }
  }, [sutraApiKey]);
  
  useEffect(() => {
    if (typeof window !== 'undefined' && serpApiKey) {
      localStorage.setItem('serpApiKey', serpApiKey);
    }
  }, [serpApiKey]);
  
  // Clear API keys
  const clearApiKey = (type: 'sutra' | 'serp') => {
    if (type === 'sutra') {
      setSutraApiKey('');
      if (typeof window !== 'undefined') {
        localStorage.removeItem('sutraApiKey');
      }
    } else {
      setSerpApiKey('');
      if (typeof window !== 'undefined') {
        localStorage.removeItem('serpApiKey');
      }
    }
  };

  // Sample questions for news summarization
  const SAMPLE_QUESTIONS = [
    "Summarize the latest national news in Tamil",
    "What are the recent developments in Indian politics? Respond in Bengali.",
    "Summarize today's cricket headlines in Malayalam",
    "Provide business news updates from Maharashtra in Marathi"
  ];

  // Language options for the news
  const LANGUAGES = [
    { name: "English", code: "en", flag: "🇬🇧" },
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
    { name: "Urdu", code: "ur", flag: "🇮🇳" },
    { name: "French", code: "fr", flag: "🇫🇷" },
    { name: "German", code: "de", flag: "🇩🇪" },
    { name: "Spanish", code: "es", flag: "🇪🇸" },
    { name: "Japanese", code: "ja", flag: "🇯🇵" },
    { name: "Chinese", code: "zh", flag: "🇨🇳" },
  ];

  // News categories
  const CATEGORIES = [
    { name: "National", icon: "🇮🇳" },
    { name: "Regional", icon: "🏞️" },
    { name: "Global", icon: "🌎" },
    { name: "Business", icon: "💼" },
    { name: "Technology", icon: "💻" },
    { name: "Sports", icon: "⚽" },
    { name: "Cricket", icon: "🏏" },
    { name: "Bollywood", icon: "🎬" },
    { name: "Politics", icon: "🏛️" },
    { name: "Entertainment", icon: "🎭" },
    { name: "Science", icon: "🔬" },
  ];

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) {
      setError("Please enter a valid question.");
      return;
    }

    setIsLoading(true);
    setError("");
    setResponse("");
    setActiveTab("results");

    try {
      const result = await getSummary(query);
      setResponse(result);
    } catch (err: any) {
      setError(err.message || "Failed to get summary. Please try again.");
      setActiveTab("query");
    } finally {
      setIsLoading(false);
    }
  };

  // Get news summary
  const getSummary = async (queryText: string) => {
    // Add date to query
    const currentDate = new Date().toISOString().split("T")[0];
    let enhancedQuery = queryText;

    if (useSearch) {
      try {
        // Call API route to search Web Search(SerpApi)
        const searchResponse = await fetch("/api/search", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ 
            query: queryText,
            apiKey: serpApiKey || undefined
          }),
        });
        
        if (searchResponse.ok) {
          const searchResults = await searchResponse.json();
          
          if (searchResults && searchResults.length > 0) {
            let recentInfo = "\n\nRecent information from news sources:\n";
            
            searchResults.forEach((result: any, idx: number) => {
              // Include source information if available
              const source = result.source ? ` (Source: ${result.source})` : "";
              recentInfo += `\n${idx+1}. ${result.title || ""}${source}: ${result.body || ""}\n`;
            });
            
            enhancedQuery = `${queryText}\n\nToday's date is ${currentDate}.\n\nUse this recent information to provide an up-to-date response: ${recentInfo}\n\nProvide a well-formatted summary in the language requested. If no language is specified, use English.`;
          } else {
            enhancedQuery = `${queryText}\n\nToday's date is ${currentDate}. Please provide the most up-to-date information available.`;
          }
        } else {
          throw new Error("Failed to get search results");
        }
      } catch (err) {
        console.error("Search error:", err);
        // Fallback to date-enhanced query
        enhancedQuery = `${queryText}\n\nToday's date is ${currentDate}. Please provide the most up-to-date information available.`;
      }
    } else {
      enhancedQuery = `${queryText}\n\nToday's date is ${currentDate}. Please provide the most up-to-date information available.`;
    }
    enhancedQuery += `\n\nProvide a well-formatted summary in the language requested. Use Plain Text only don't use markdown.`;

    console.log(enhancedQuery);

    // Call Sutra API
    const summaryResponse = await fetch("/api/summarize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ 
        query: enhancedQuery,
        showToolCalls,
        apiKey: sutraApiKey || undefined
      }),
    });

    if (!summaryResponse.ok) {
      const errorData = await summaryResponse.json();
      throw new Error(errorData.error || "Failed to get summary");
    }

    const data = await summaryResponse.json();
    return data.response;
  };

  // Reset form
  const resetForm = () => {
    setQuery("");
    setResponse("");
    setError("");
    setActiveTab("query");
  };

  // Set sample question
  const setQuestion = (question: string) => {
    setQuery(question);
  };

  // Create a query with language and category
  const createQuery = (language: string, category: string) => {
    const query = `Summarize today's top ${category} news in ${language}`;
    setQuery(query);
  };

  // Enhanced UI for Indian languages selection
  const renderLanguageSelector = () => {
    return (
      <div className="w-full">
        <h3 className="text-sm font-medium mb-2 flex items-center">
          <Languages className="h-4 w-4 mr-2" /> Indian Languages
        </h3>
        <div className="flex flex-wrap gap-2 mb-3">
          {LANGUAGES.filter(lang => lang.flag === "🇮🇳").map((lang) => (
            <Badge 
              key={lang.code} 
              variant="outline" 
              className="cursor-pointer hover:bg-accent"
              onClick={() => createQuery(lang.name, "National")}
            >
              {lang.flag} {lang.name}
            </Badge>
          ))}
        </div>
        <h3 className="text-sm font-medium mb-2 flex items-center">
          <Languages className="h-4 w-4 mr-2" /> Other Languages
        </h3>
        <div className="flex flex-wrap gap-2">
          {LANGUAGES.filter(lang => lang.flag !== "🇮🇳").map((lang) => (
            <Badge 
              key={lang.code} 
              variant="outline" 
              className="cursor-pointer hover:bg-accent"
              onClick={() => createQuery(lang.name, "Global")}
            >
              {lang.flag} {lang.name}
            </Badge>
          ))}
        </div>
      </div>
    );
  };

  // Enhanced UI for categories selection
  const renderCategorySelector = () => {
    return (
      <div className="w-full">
        <h3 className="text-sm font-medium mb-2 flex items-center">
          <Newspaper className="h-4 w-4 mr-2" /> India-Specific Categories
        </h3>
        <div className="flex flex-wrap gap-2 mb-3">
          {CATEGORIES.filter(cat => ["National", "Regional", "Cricket", "Bollywood"].includes(cat.name)).map((category) => (
            <Badge 
              key={category.name} 
              variant="secondary" 
              className="cursor-pointer hover:bg-accent"
              onClick={() => createQuery("Hindi", category.name)}
            >
              {category.icon} {category.name}
            </Badge>
          ))}
        </div>
        <h3 className="text-sm font-medium mb-2 flex items-center">
          <Newspaper className="h-4 w-4 mr-2" /> Other Categories
        </h3>
        <div className="flex flex-wrap gap-2">
          {CATEGORIES.filter(cat => !["National", "Regional", "Cricket", "Bollywood"].includes(cat.name)).map((category) => (
            <Badge 
              key={category.name} 
              variant="secondary" 
              className="cursor-pointer hover:bg-accent"
              onClick={() => createQuery("English", category.name)}
            >
              {category.icon} {category.name}
            </Badge>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="container mx-auto p-4 max-w-6xl">
      <header className="flex justify-between items-center py-6 border-b">
        <div className="flex items-center space-x-4">
          <Image
            src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png"
            alt="Sutra Logo"
            width={40}
            height={40}
          />
          <div>
            <h1 className="text-2xl font-bold">Indian Multilingual News Summarizer</h1>
            <p className="text-muted-foreground">Get news in 50+ languages</p>
            <div className="flex flex-wrap gap-3 text-xs text-muted-foreground mt-1 items-center">
              <div className="flex items-center gap-1">
                <span className={`inline-block w-2 h-2 ${sutraApiKey ? "bg-green-500" : "bg-red-500"} rounded-full`}></span>
                <span>Sutra API</span>
              </div>
              <div className="flex items-center gap-1">
                <span className={`inline-block w-2 h-2 ${serpApiKey ? "bg-green-500" : "bg-red-500"} rounded-full`}></span>
                <span>SerpAPI</span>
              </div>
              {(!sutraApiKey || !serpApiKey) && (
                <Button variant="link" size="sm" className="text-xs p-0 h-auto text-blue-500" onClick={() => document.getElementById('settings-trigger')?.click()}>
                  Set API Keys
                </Button>
              )}
            </div>
          </div>
        </div>
        
        <Sheet>
          <SheetTrigger asChild>
            <Button id="settings-trigger" variant="outline" size="icon">
              <Settings className="h-4 w-4" />
            </Button>
          </SheetTrigger>
          <SheetContent>
            <SheetHeader>
              <SheetTitle>Settings</SheetTitle>
              <SheetDescription>
                Configure your news summarization preferences
              </SheetDescription>
            </SheetHeader>
            <div className="space-y-6 py-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="useSearch">Search for recent information</Label>
                  <Switch
                    id="useSearch"
                    checked={useSearch}
                    onCheckedChange={setUseSearch}
                  />
                </div>
                <p className="text-sm text-muted-foreground">
                  Uses Web Search(SerpApi) to find the latest news before generating summaries
                </p>
              </div>
              <Separator />
              <div className="space-y-2">
                <h3 className="text-sm font-medium">API Keys</h3>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <Label htmlFor="sutraApiKey">Sutra API Key</Label>
                      {sutraApiKey && <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">Set</Badge>}
                    </div>
                    <div className="flex gap-2">
                      <input
                        id="sutraApiKey"
                        type="password"
                        className="w-full px-3 py-2 border rounded-md text-sm"
                        value={sutraApiKey}
                        onChange={(e) => setSutraApiKey(e.target.value)}
                        placeholder="Enter your Sutra API key"
                      />
                      {sutraApiKey && (
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => clearApiKey('sutra')}
                        >
                          Clear
                        </Button>
                      )}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      <a href="https://www.two.ai/sutra/api" target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
                        Get your API key from Two AI Sutra
                      </a>
                    </p>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <Label htmlFor="serpApiKey">SerpAPI Key</Label>
                      {serpApiKey && <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">Set</Badge>}
                    </div>
                    <div className="flex gap-2">
                      <input
                        id="serpApiKey"
                        type="password"
                        className="w-full px-3 py-2 border rounded-md text-sm"
                        value={serpApiKey}
                        onChange={(e) => setSerpApiKey(e.target.value)}
                        placeholder="Enter your SerpAPI key"
                      />
                      {serpApiKey && (
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => clearApiKey('serp')}
                        >
                          Clear
                        </Button>
                      )}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      <a href="https://serpapi.com/" target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
                        Get your SerpAPI key
                      </a>
                    </p>
                  </div>
                </div>
              </div>
              <Separator />
              <div className="space-y-2">
                <h3 className="text-sm font-medium">About</h3>
                <p className="text-sm text-muted-foreground">
                  This application uses SUTRA AI to generate multilingual news summaries across various categories.
                </p>
              </div>
            </div>
          </SheetContent>
        </Sheet>
      </header>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="mt-6">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="query">Query</TabsTrigger>
          <TabsTrigger value="results">Results</TabsTrigger>
        </TabsList>
        <TabsContent value="query">
          <Card>
            <CardHeader>
              <CardTitle>Ask for News Summaries</CardTitle>
              <CardDescription>
                Request news summaries in any language across different categories
              </CardDescription>
            </CardHeader>
            <CardContent>
              {error && (
                <Alert variant="destructive" className="mb-4">
                  <AlertCircle className="h-4 w-4" />
                  <AlertTitle>Error</AlertTitle>
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}
              
              {!sutraApiKey && (
                <Alert className="mb-4 border-blue-200 bg-blue-50">
                  <AlertCircle className="h-4 w-4 text-blue-500" />
                  <AlertTitle className="text-blue-700">Sutra API Key Required</AlertTitle>
                  <AlertDescription className="text-blue-600">
                    Please set your Sutra API key in the settings to use the application.{" "}
                    <a 
                      href="https://www.two.ai/sutra/api" 
                      target="_blank" 
                      rel="noopener noreferrer" 
                      className="text-blue-600 font-medium hover:underline"
                    >
                      Get your API key
                    </a>
                  </AlertDescription>
                </Alert>
              )}
              
              {useSearch && !serpApiKey && (
                <Alert className="mb-4 border-yellow-200 bg-yellow-50">
                  <AlertCircle className="h-4 w-4 text-yellow-500" />
                  <AlertTitle className="text-yellow-700">SerpAPI Key Required for Search</AlertTitle>
                  <AlertDescription className="text-yellow-600">
                    You have search enabled but no SerpAPI key. Please add your key in settings or disable search.{" "}
                    <a 
                      href="https://serpapi.com/" 
                      target="_blank" 
                      rel="noopener noreferrer" 
                      className="text-yellow-600 font-medium hover:underline"
                    >
                      Get your API key
                    </a>
                  </AlertDescription>
                </Alert>
              )}
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <Textarea
                  placeholder="e.g., Summarize today's top business news in French."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="min-h-[120px]"
                />
                <Button type="submit" className="w-full" disabled={isLoading}>
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Processing...
                    </>
                  ) : (
                    <>
                      Get Summary <ArrowRight className="ml-2 h-4 w-4" />
                    </>
                  )}
                </Button>
              </form>
            </CardContent>
            <CardFooter className="flex-col items-start space-y-4">
              <div className="w-full">
                <h3 className="text-sm font-medium mb-2">Sample questions</h3>
                <div className="space-y-2">
                  {SAMPLE_QUESTIONS.map((question, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      className="w-full justify-start text-left"
                      onClick={() => setQuestion(question)}
                    >
                      {question}
                    </Button>
                  ))}
                </div>
              </div>
              
              {renderLanguageSelector()}
              
              {renderCategorySelector()}
            </CardFooter>
          </Card>
        </TabsContent>
        
        <TabsContent value="results">
          <Card>
            <CardHeader>
              <CardTitle>
                {response ? "📰 News Summary" : "No Results Yet"}
              </CardTitle>
              <CardDescription>
                {response
                  ? "Here's your multilingual news summary"
                  : "Submit a query to get news summaries"}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <div className="flex items-center justify-center p-12">
                  <Loader2 className="h-8 w-8 animate-spin text-primary" />
                </div>
              ) : response ? (
                <>
                  {useSearch && (
                    <Alert className="mb-4">
                      <AlertCircle className="h-4 w-4" />
                      <AlertTitle>Search-Enhanced Summary</AlertTitle>
                      <AlertDescription>
                        This summary includes recent information from web search results
                      </AlertDescription>
                    </Alert>
                  )}
                  <div className="prose prose-neutral max-w-none dark:prose-invert">
                    <div dangerouslySetInnerHTML={{ __html: response.replace(/\n\n/g, '<br><br>') }} />
                  </div>
                </>
              ) : (
                <div className="text-center p-12 text-muted-foreground">
                  <Newspaper className="h-12 w-12 mx-auto mb-4 opacity-20" />
                  <p>No summary to display yet. Please submit a query.</p>
                </div>
              )}
            </CardContent>
            {response && (
              <CardFooter>
                <Button onClick={resetForm} variant="outline">New Query</Button>
              </CardFooter>
            )}
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
