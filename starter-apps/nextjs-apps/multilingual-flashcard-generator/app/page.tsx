"use client";

import { useState, useEffect } from "react";
import { Flashcard, FlashcardGenerationParams } from "@/types";
import { generateFlashcards } from "@/utils/flashcardGenerator";
import ErrorMessage from "@/components/ErrorMessage";
import FlashcardForm from "@/components/FlashcardForm";
import FlashcardViewer from "@/components/FlashcardViewer";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ExternalLink, Key, Languages, Moon, Sun } from "lucide-react";

export default function FlashcardApp() {
  const [currentView, setCurrentView] = useState<"generator" | "flashcards">(
    "generator"
  );
  const [isGenerating, setIsGenerating] = useState(false);
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [sourceLanguage, setSourceLanguage] = useState("en");
  const [targetLanguage, setTargetLanguage] = useState("es");
  const [error, setError] = useState<string | null>(null);
  const [apiKey, setApiKey] = useState("");
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    // Check for saved theme preference or default to light mode
    const savedTheme = localStorage.getItem("theme");
    const prefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches;

    if (savedTheme === "dark" || (!savedTheme && prefersDark)) {
      setIsDark(true);
      document.documentElement.classList.add("dark");
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = !isDark;
    setIsDark(newTheme);

    if (newTheme) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  };

  const handleGenerateFlashcards = async (
    params: FlashcardGenerationParams
  ) => {
    if (!apiKey.trim()) {
      setError("Please enter your SUTRA API key first");
      return;
    }

    setIsGenerating(true);
    setError(null);
    setSourceLanguage(params.sourceLanguage);
    setTargetLanguage(params.targetLanguage);

    try {
      const generatedFlashcards = await generateFlashcards({
        ...params,
        apiKey,
      });

      if (!generatedFlashcards || generatedFlashcards.length === 0) {
        throw new Error(
          "No flashcards were generated. Please try a different input or check your API key."
        );
      }

      setFlashcards(generatedFlashcards);
      setCurrentView("flashcards");
    } catch (error: unknown) {
      // Provide a more specific error message based on the error
      let errorMessage =
        "Failed to generate flashcards. Please check your API key and try again.";

      if (error instanceof Error) {
        if (error.message.includes("API key")) {
          errorMessage =
            "Invalid API key. Please check that you've entered a valid SUTRA API key.";
        } else if (error.message.includes("No flashcards")) {
          errorMessage = error.message;
        } else if (error.message.includes("Failed to fetch")) {
          errorMessage =
            "Network error. Please check your internet connection and try again.";
        }
      }

      setError(errorMessage);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleBackToGenerator = () => {
    setCurrentView("generator");
    setError(null);
  };

  if (currentView === "flashcards") {
    return (
      <FlashcardViewer
        flashcards={flashcards}
        sourceLanguage={sourceLanguage}
        targetLanguage={targetLanguage}
        onBack={handleBackToGenerator}
        isDark={isDark}
        toggleTheme={toggleTheme}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-white to-purple-50 dark:from-gray-950 dark:via-gray-900 dark:to-violet-950">
      {/* Header */}
      <div className="relative overflow-hidden bg-gradient-to-r from-violet-600 via-purple-600 to-indigo-600 dark:from-violet-800 dark:via-purple-800 dark:to-indigo-800">
        <div className="absolute inset-0 bg-black/10" />
        <div className="relative container mx-auto px-4 py-16 text-center">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-3 bg-white/20 rounded-2xl backdrop-blur-sm">
              <Languages className="h-8 w-8 text-white" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-white">
              Multilingual Flashcard Generator
            </h1>
          </div>
          <p className="text-xl text-white/90 max-w-2xl mx-auto">
            Create language learning flashcards with AI-powered translations
          </p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* API Key Section */}
        <Card className="mb-8 border-0 shadow-lg bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
          <CardHeader className="pb-4">
            <div className="flex items-center gap-2">
              <Key className="h-5 w-5 text-violet-600" />
              <CardTitle className="text-lg">API Configuration</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="flex gap-3">
              <div className="flex-1">
                <Input
                  placeholder="Enter your SUTRA API key"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  type="password"
                  className="h-11"
                />
              </div>
              <Button
                variant="outline"
                className="h-11 px-6"
                onClick={() =>
                  window.open("https://www.two.ai/sutra", "_blank")
                }
              >
                <ExternalLink className="h-4 w-4 mr-2" />
                Get Key
              </Button>
            </div>
            <p className="text-sm text-muted-foreground mt-2">
              Your API key is required to generate flashcards with SUTRA
            </p>
          </CardContent>
        </Card>

        {error && <ErrorMessage message={error} />}

        {/* Generator Form */}
        <FlashcardForm
          onGenerateFlashcards={handleGenerateFlashcards}
          isGenerating={isGenerating}
          isDark={isDark}
        />
      </div>

      {/* Theme Toggle */}
      <Button
        variant="outline"
        size="icon"
        className="fixed bottom-6 left-6 h-12 w-12 rounded-full shadow-lg"
        onClick={toggleTheme}
      >
        <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
        <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
        <span className="sr-only">Toggle theme</span>
      </Button>
    </div>
  );
}
