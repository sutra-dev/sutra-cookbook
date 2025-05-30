import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  ArrowLeft,
  ArrowRight,
  RotateCcw,
  Check,
  X,
  Moon,
  Sun,
  Loader2,
} from "lucide-react";
import { Flashcard } from "@/types";
import { LANGUAGES } from "@/constants";
import { Badge } from "@/components/ui/badge";

interface FlashcardViewerProps {
  flashcards: Flashcard[];
  sourceLanguage: string;
  targetLanguage: string;
  onBack: () => void;
  isDark?: boolean;
  toggleTheme?: () => void;
}

export default function FlashcardViewer({
  flashcards,
  sourceLanguage,
  targetLanguage,
  onBack,
  toggleTheme,
}: FlashcardViewerProps) {
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [knownCards, setKnownCards] = useState<Set<number>>(new Set());
  const [isAnimating, setIsAnimating] = useState(false);

  // Check if flashcards array is empty
  if (!flashcards || flashcards.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-violet-50 via-white to-purple-50 dark:from-gray-950 dark:via-gray-900 dark:to-violet-950 flex flex-col items-center justify-center">
        <div className="text-center p-8 max-w-md">
          <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-violet-600" />
          <h2 className="text-2xl font-bold mb-2">No flashcards available</h2>
          <p className="mb-6 text-slate-600 dark:text-slate-400">
            There was a problem loading your flashcards. Please go back and try
            again.
          </p>
          <Button
            onClick={onBack}
            className="bg-gradient-to-r from-violet-600 to-purple-600"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Generator
          </Button>
        </div>

        {/* Theme Toggle */}
        {toggleTheme && (
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
        )}
      </div>
    );
  }

  const currentCard = flashcards[currentCardIndex];
  const progress = (knownCards.size / flashcards.length) * 100;

  const nextCard = () => {
    if (isAnimating || currentCardIndex >= flashcards.length - 1) return;

    setIsAnimating(true);
    setTimeout(() => {
      setCurrentCardIndex(currentCardIndex + 1);
      setIsFlipped(false);
      setIsAnimating(false);
    }, 300);
  };

  const prevCard = () => {
    if (isAnimating || currentCardIndex <= 0) return;

    setIsAnimating(true);
    setTimeout(() => {
      setCurrentCardIndex(currentCardIndex - 1);
      setIsFlipped(false);
      setIsAnimating(false);
    }, 300);
  };

  const flipCard = () => {
    if (isAnimating) return;
    setIsFlipped(!isFlipped);
  };

  const markAsKnown = () => {
    const newKnownCards = new Set(knownCards);
    newKnownCards.add(currentCardIndex);
    setKnownCards(newKnownCards);

    if (currentCardIndex < flashcards.length - 1) {
      nextCard();
    }
  };

  const markAsUnknown = () => {
    const newKnownCards = new Set(knownCards);
    newKnownCards.delete(currentCardIndex);
    setKnownCards(newKnownCards);

    if (currentCardIndex < flashcards.length - 1) {
      nextCard();
    }
  };

  const getLanguageName = (code: string) => {
    return LANGUAGES.find((lang) => lang.code === code)?.name || code;
  };

  const cardTransitionClass = isFlipped ? "rotate-y-180" : "";

  // Make sure currentCard is available
  if (!currentCard) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-violet-50 via-white to-purple-50 dark:from-gray-950 dark:via-gray-900 dark:to-violet-950 flex flex-col items-center justify-center">
        <div className="text-center p-8 max-w-md">
          <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-violet-600" />
          <h2 className="text-2xl font-bold mb-2">Loading flashcards</h2>
          <p className="mb-6 text-slate-600 dark:text-slate-400">
            Please wait while we prepare your flashcards...
          </p>
          <Button onClick={onBack} variant="outline">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Generator
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-white to-purple-50 dark:from-gray-950 dark:via-gray-900 dark:to-violet-950">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between mb-8">
          <Button
            variant="outline"
            onClick={onBack}
            className="mb-4 md:mb-0 text-slate-600 dark:text-slate-300 hover:text-slate-900 -ml-2 pl-0"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Generator
          </Button>

          <div className="flex items-center gap-4">
            <Badge
              variant="outline"
              className="px-3 py-1.5 border-violet-200 dark:border-violet-800 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm"
            >
              <span className="text-violet-700 dark:text-violet-300 font-medium">
                {getLanguageName(sourceLanguage)} →{" "}
                {getLanguageName(targetLanguage)}
              </span>
            </Badge>

            <Badge
              variant="outline"
              className="px-3 py-1.5 border-violet-200 dark:border-violet-800 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm"
            >
              <span className="text-violet-700 dark:text-violet-300 font-medium">
                {flashcards.length} cards
              </span>
            </Badge>
          </div>
        </div>

        {/* Progress and Stats */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-slate-600 dark:text-slate-400">
              Card {currentCardIndex + 1} of {flashcards.length}
            </span>
            <div className="flex items-center gap-2">
              <span className="text-sm text-slate-600 dark:text-slate-400">
                Mastered:
              </span>
              <Badge variant="secondary" className="font-medium">
                {knownCards.size}/{flashcards.length}
              </Badge>
            </div>
          </div>

          {/* Progress bar */}
          <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 overflow-hidden">
            <div
              className="bg-gradient-to-r from-violet-600 to-purple-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Main content */}
        <div className="max-w-2xl mx-auto flex flex-col items-center">
          {/* Flashcard */}
          <div
            className="relative w-full aspect-[4/3] max-h-[400px] mb-8 cursor-pointer perspective-1000"
            onClick={flipCard}
          >
            <div
              className={`relative w-full h-full transition-all duration-500 transform-style-preserve-3d ${cardTransitionClass}`}
            >
              {/* Front */}
              <Card
                className="absolute inset-0 w-full h-full backface-hidden bg-white dark:bg-gray-800 
                shadow-lg border-0 hover:shadow-xl transition-shadow rounded-xl overflow-hidden"
              >
                <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-violet-600 to-purple-600"></div>
                <CardContent className="flex flex-col items-center justify-center h-full p-6 md:p-8 text-center">
                  <div className="absolute top-3 left-3 px-3 py-1 bg-violet-100 dark:bg-violet-900/30 rounded-md text-sm font-medium text-violet-700 dark:text-violet-300">
                    {getLanguageName(sourceLanguage)}
                  </div>

                  {knownCards.has(currentCardIndex) && (
                    <div className="absolute top-3 right-3 bg-green-100 dark:bg-green-900/30 p-1 rounded-full">
                      <Check className="h-4 w-4 text-green-600 dark:text-green-400" />
                    </div>
                  )}

                  <div className="text-2xl md:text-3xl font-semibold text-slate-800 dark:text-slate-100 mb-4 mt-4">
                    {currentCard?.front}
                  </div>

                  <div className="text-xs text-slate-500 dark:text-slate-400 font-medium mt-4 bg-slate-50 dark:bg-slate-700/50 px-3 py-1 rounded-full flex items-center">
                    <RotateCcw className="h-3 w-3 mr-1.5 text-slate-400 dark:text-slate-500" />
                    Click to reveal translation
                  </div>
                </CardContent>
              </Card>

              {/* Back */}
              <Card
                className="absolute inset-0 w-full h-full backface-hidden rotate-y-180 bg-white dark:bg-gray-800 
                shadow-lg border-0 hover:shadow-xl transition-shadow rounded-xl overflow-hidden"
              >
                <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-violet-600 to-purple-600"></div>
                <CardContent className="flex flex-col items-center justify-center h-full p-6 md:p-8 text-center">
                  <div className="absolute top-3 left-3 px-3 py-1 bg-purple-100 dark:bg-purple-900/30 rounded-md text-sm font-medium text-purple-700 dark:text-purple-300">
                    {getLanguageName(targetLanguage)}
                  </div>

                  {knownCards.has(currentCardIndex) && (
                    <div className="absolute top-3 right-3 bg-green-100 dark:bg-green-900/30 p-1 rounded-full">
                      <Check className="h-4 w-4 text-green-600 dark:text-green-400" />
                    </div>
                  )}

                  <div className="text-2xl md:text-3xl font-semibold text-violet-700 dark:text-violet-300 mb-2 mt-4">
                    {currentCard?.back}
                  </div>

                  {currentCard?.example && (
                    <div className="mt-4 p-4 bg-gradient-to-r from-violet-50/80 to-purple-50/80 dark:from-violet-900/20 dark:to-purple-900/20 rounded-lg text-sm text-slate-600 dark:text-slate-300 max-w-md">
                      {currentCard.example}
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Card Controls */}
          <div className="w-full flex flex-col sm:flex-row items-center gap-4 sm:justify-between">
            {/* Navigation */}
            <div className="flex items-center gap-3">
              <Button
                variant="outline"
                onClick={prevCard}
                disabled={currentCardIndex === 0}
                className="h-11 w-11 rounded-full p-0 border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-gray-800/90"
              >
                <ArrowLeft className="w-4 h-4" />
              </Button>

              <Button
                variant="outline"
                onClick={flipCard}
                className="h-11 px-5 border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-gray-800/90"
              >
                <RotateCcw className="w-4 h-4 mr-2" />
                Flip
              </Button>

              <Button
                variant="outline"
                onClick={nextCard}
                disabled={currentCardIndex === flashcards.length - 1}
                className="h-11 w-11 rounded-full p-0 border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-gray-800/90"
              >
                <ArrowRight className="w-4 h-4" />
              </Button>
            </div>

            {/* Knowledge marking */}
            <div className="flex items-center gap-3">
              <Button
                variant="outline"
                onClick={markAsUnknown}
                className="h-11 border-red-200 dark:border-red-900/50 bg-white/90 dark:bg-gray-800/90 hover:bg-red-50 dark:hover:bg-red-900/20 text-red-600 dark:text-red-400"
              >
                <X className="w-4 h-4 mr-2" />
                Don&apos;t Know
              </Button>

              <Button
                variant="outline"
                onClick={markAsKnown}
                className="h-11 border-green-200 dark:border-green-900/50 bg-white/90 dark:bg-gray-800/90 hover:bg-green-50 dark:hover:bg-green-900/20 text-green-600 dark:text-green-400"
              >
                <Check className="w-4 h-4 mr-2" />
                Know It
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Theme Toggle */}
      {toggleTheme && (
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
      )}

      {/* Add CSS for card flipping */}
      <style jsx global>{`
        .perspective-1000 {
          perspective: 1000px;
        }

        .transform-style-preserve-3d {
          transform-style: preserve-3d;
        }

        .backface-hidden {
          backface-visibility: hidden;
        }

        .rotate-y-180 {
          transform: rotateY(180deg);
        }
      `}</style>
    </div>
  );
}
