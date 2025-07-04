"use client";

import { useState, useEffect } from "react";
import { Search, Globe, Loader2, Newspaper, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { NewsCard } from "@/components/news-card";
import { NewsCardSkeleton } from "@/components/news-card-skeleton";
import { SettingsDialog } from "@/components/settings-dialog";
import { newsApi, NewsItem } from "@/lib/api";
import { useApiKeys } from "@/lib/hooks/use-api-keys";
import Image from "next/image";

export default function Home() {
  const [query, setQuery] = useState("latest AI news");
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [languages, setLanguages] = useState<string[]>([]);
  const [selectedLanguage, setSelectedLanguage] = useState("English");
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [currentPage, setCurrentPage] = useState(1);
  const [hasMoreNews, setHasMoreNews] = useState(true);
  const [autoLoadQueries] = useState([
    "latest technology news", "breaking news today", "world news updates", 
    "science discoveries", "business news", "health updates"
  ]);

  // Get API keys from user settings or environment variables
  const { apiKeys, hasSerperKey, hasSutraKey, isLoaded } = useApiKeys();

  // Auto-load initial news
  const loadInitialNews = async () => {
    setCurrentPage(1);
    setNews([]);
    setHasMoreNews(true);
    setError(null);
    await loadMoreNews(1, true);
  };

  // Load more news with smart buffering
  const loadMoreNews = async (page: number = currentPage, isInitial: boolean = false) => {
    if (isInitial) {
      setInitialLoading(true);
    } else {
      setLoadingMore(true);
    }

    try {
      // Get a rotating query for variety
      const queryIndex = (page - 1) % autoLoadQueries.length;
      const searchQuery = autoLoadQueries[queryIndex];

             const response = await newsApi.searchNews({
         query: searchQuery,
         num_results: 5, // Minimum allowed by API (5-30 range)
         page: page, // Add page parameter for pagination
         serper_api_key: apiKeys.serperApiKey,
         translate_to: selectedLanguage !== "English" ? selectedLanguage : undefined,
         sutra_api_key: selectedLanguage !== "English" ? apiKeys.sutraApiKey : undefined,
       });

      if (response.news && response.news.length > 0) {
        setNews(prev => isInitial ? response.news : [...prev, ...response.news]);
        setCurrentPage(page + 1);
        
        // Check if we should continue loading (stop after many pages to prevent infinite requests)
        if (page >= 10) {
          setHasMoreNews(false);
        }
      } else {
        setHasMoreNews(false);
      }
    } catch (err: any) {
      console.error("Load more news error:", err);
      if (!isInitial) {
        setError("Failed to load more news. Please check your connection.");
      }
    } finally {
      if (isInitial) {
        setInitialLoading(false);
      } else {
        setLoadingMore(false);
      }
    }
  };

  useEffect(() => {
    // Check API health and auto-load initial news
    const checkApiHealth = async () => {
      try {
        await newsApi.healthCheck();
        setApiStatus('online');
        
        // Load languages only if API is online
        try {
          const langs = await newsApi.getLanguages();
          setLanguages(langs);
        } catch (error) {
          console.error("Failed to load languages:", error);
          // Set default languages if API fails
          setLanguages([
            "English", "Hindi", "Spanish", "French", "German", 
            "Chinese", "Japanese", "Korean", "Arabic", "Portuguese"
          ]);
        }

        // Auto-load initial news if API keys are available
        if (isLoaded && hasSerperKey) {
          await loadInitialNews();
        }
      } catch (error) {
        console.error("API is offline:", error);
        setApiStatus('offline');
        setError("Cannot connect to the news API. Please ensure the backend is running on http://localhost:8000");
      } finally {
        setInitialLoading(false);
      }
    };

    if (isLoaded) {
      checkApiHealth();
    }
  }, [isLoaded, hasSerperKey]);

  // Auto-load news when language changes
  useEffect(() => {
    if (apiStatus === 'online' && hasSerperKey && news.length > 0) {
      // Reload news when language changes
      loadInitialNews();
    }
  }, [selectedLanguage]);

  // Intersection observer for infinite scroll
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const target = entries[0];
        if (target.isIntersecting && hasMoreNews && !loadingMore && !initialLoading && hasSerperKey) {
          loadMoreNews();
        }
      },
      { threshold: 0.1 }
    );

    const scrollTrigger = document.getElementById('scroll-trigger');
    if (scrollTrigger) {
      observer.observe(scrollTrigger);
    }

    return () => {
      if (scrollTrigger) {
        observer.unobserve(scrollTrigger);
      }
    };
  }, [hasMoreNews, loadingMore, initialLoading, hasSerperKey]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isLoaded) {
      setError("Loading API settings...");
      return;
    }
    
    if (apiStatus === 'offline') {
      setError("Cannot connect to the news API. Please ensure the backend is running.");
      return;
    }

    if (!hasSerperKey) {
      setError("Serper API key is missing. Please configure your API keys in the settings.");
      return;
    }

    if (selectedLanguage !== "English" && !hasSutraKey) {
      setError("Sutra API key is required for translation. Please configure your API keys in the settings or select English.");
      return;
    }

    setLoading(true);
    setError(null);
    setNews([]);
    setCurrentPage(1);
    setHasMoreNews(true);

    try {
      const response = await newsApi.searchNews({
        query,
        num_results: 10, // Use valid range (5-30)
        page: 1, // Always start from page 1 for manual search
        serper_api_key: apiKeys.serperApiKey,
        translate_to: selectedLanguage !== "English" ? selectedLanguage : undefined,
        sutra_api_key: selectedLanguage !== "English" ? apiKeys.sutraApiKey : undefined,
      });

      setNews(response.news);
      setCurrentPage(2); // Ready for next page if user scrolls
    } catch (err: any) {
      console.error("Search error:", err);
      if (err.code === 'ERR_NETWORK') {
        setError("Cannot connect to the news API. Please ensure the backend is running on http://localhost:8000");
      } else {
        setError(err.response?.data?.detail || "Failed to fetch news. Please check your API keys.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 glass-header border-b border-border/50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="relative w-12 h-12 rounded-xl overflow-hidden shadow-md">
                <Image
                  src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png"
                  alt="Logo"
                  fill
                  className="object-contain"
                />
              </div>
              <div>
              <h1 className="text-2xl font-bold text-gradient">
                Global News Hub
              </h1>
                <p className="text-xs text-muted-foreground hidden sm:block">
                  AI-powered multilingual news platform
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <div className="relative">
                <Globe className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
              <select
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                  className="pl-10 pr-8 py-2 rounded-lg border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all appearance-none cursor-pointer hover:border-primary/50 min-w-[140px]"
                disabled={languages.length === 0}
              >
                {languages.map((lang) => (
                  <option key={lang} value={lang}>
                    {lang}
                  </option>
                ))}
              </select>
              </div>
              
              <SettingsDialog />
              
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-muted/50">
                <div className={`w-2 h-2 rounded-full ${
                  apiStatus === 'online' ? 'bg-green-500' : 
                  apiStatus === 'offline' ? 'bg-red-500' : 
                  'bg-yellow-500'
                }`} />
                <span className="text-xs font-medium">
                  {apiStatus === 'online' ? 'Online' : apiStatus === 'offline' ? 'Offline' : 'Checking'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* API Status Alert */}
      {apiStatus === 'offline' && (
        <div className="bg-destructive/10 border-b border-destructive/20">
          <div className="container mx-auto px-4 py-3">
            <div className="flex items-center gap-2 text-sm text-destructive">
              <AlertCircle className="h-4 w-4" />
              <span>API is offline. Please start the backend server with: <code className="ml-2 bg-black/10 px-2 py-1 rounded">uvicorn api:app --reload</code></span>
            </div>
          </div>
        </div>
      )}

      {/* Hero Section with Search */}
      <section className="relative py-16 px-4">
        <div className="container mx-auto max-w-4xl">
          <div className="text-center mb-8">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Global News in{" "}
              <span className="text-gradient">50+ Languages</span>
            </h2>
            <p className="text-lg text-muted-foreground">
              Latest news auto-loaded and translated by AI • Search for specific topics below
            </p>
          </div>

          <form onSubmit={handleSearch} className="relative">
            <div className="flex gap-3">
              <div className="relative flex-1">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Search for specific topics (optional)..."
                  className="w-full pl-12 pr-4 py-4 rounded-xl border border-border bg-background text-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all hover:border-primary/50 shadow-sm"
                />
              </div>
              <Button
                type="submit"
                size="lg"
                disabled={loading || apiStatus === 'offline' || !isLoaded || !hasSerperKey}
                className="px-8 rounded-xl shadow-md hover:shadow-lg transition-all"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    Searching...
                  </>
                ) : (
                  <>
                    <Search className="mr-2 h-5 w-5" />
                    Search
                  </>
                )}
              </Button>
            </div>
          </form>

          {error && (
            <div className="mt-6 p-4 rounded-xl bg-destructive/10 border border-destructive/20 text-destructive animate-in slide-in-from-top-2 duration-300">
              <div className="flex items-start gap-3">
                <AlertCircle className="h-5 w-5 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="font-medium">Error</p>
                  <p className="text-sm mt-1 opacity-90">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* API Keys Status Alert */}
          {isLoaded && !hasSerperKey && (
            <div className="mt-6 p-4 rounded-xl bg-blue-50 border border-blue-200 animate-in slide-in-from-top-2 duration-300">
              <div className="flex items-start gap-3">
                <AlertCircle className="h-5 w-5 mt-0.5 flex-shrink-0 text-blue-600" />
                <div className="text-blue-800">
                  <p className="font-medium">Configuration Required</p>
                  <p className="text-sm mt-1 opacity-90">
                    Please configure your API keys in settings to start searching for news.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </section>

            {/* News Grid */}
      <section className="px-4 pb-16">
        <div className="container mx-auto">
          {initialLoading ? (
            <div className="space-y-8">
              <div className="text-center">
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-muted/50 rounded-full text-sm text-muted-foreground">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Loading latest news...
                </div>
              </div>
              <div className="space-y-12">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="max-w-3xl mx-auto">
                    <NewsCardSkeleton />
                  </div>
                ))}
              </div>
            </div>
          ) : news.length > 0 ? (
            <>
              <div className="mb-8 text-center">
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-muted/50 rounded-full text-sm text-muted-foreground">
                  <Globe className="h-4 w-4" />
                  <span>Reading in {selectedLanguage}</span>
                  <span>•</span>
                  <span>{news.length} articles loaded</span>
                </div>
              </div>
              
              {/* Single News Feed */}
              <div className="space-y-12">
                {news.map((item, index) => (
                  <div key={`${item.link}-${index}`} className="max-w-3xl mx-auto">
                    <div className="relative">
                      {/* Article counter */}
                      <div className="absolute -left-4 top-4 z-10">
                        <div className="w-8 h-8 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-sm font-semibold">
                          {index + 1}
                        </div>
                      </div>
                      <NewsCard news={item} />
                    </div>
                    
                    {/* Separator line */}
                    {index < news.length - 1 && (
                      <div className="mt-12 flex items-center justify-center">
                        <div className="h-px bg-border w-32"></div>
                        <div className="mx-4 text-xs text-muted-foreground">•</div>
                        <div className="h-px bg-border w-32"></div>
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Infinite scroll trigger */}
              <div id="scroll-trigger" className="mt-8 flex justify-center">
                {loadingMore ? (
                  <div className="flex items-center gap-2 px-4 py-3 bg-muted/50 rounded-full text-sm text-muted-foreground">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Loading more news...
                  </div>
                ) : hasMoreNews ? (
                  <div className="text-xs text-muted-foreground">
                    Scroll down for more news
                  </div>
                ) : (
                  <div className="text-xs text-muted-foreground">
                    You've reached the end • Search above for specific topics
                  </div>
                )}
              </div>
            </>
          ) : !initialLoading && (
            <div className="text-center py-20">
              <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-muted/50 flex items-center justify-center">
                <Newspaper className="h-12 w-12 text-muted-foreground" />
              </div>
              <h3 className="text-xl font-semibold mb-3">No news available</h3>
              <p className="text-muted-foreground max-w-md mx-auto leading-relaxed">
                Unable to load news at the moment. Try searching for specific topics above.
              </p>
              {!hasSerperKey && (
                <p className="text-sm text-primary mt-4">
                  Configure your API keys in settings to get started
                </p>
              )}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
