import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { CONTENT_FOCUS, LANGUAGES } from "@/constants";
import { FlashcardGenerationParams } from "@/types";
import {
  BookOpen,
  Globe,
  RefreshCw,
  Sparkles,
  Target,
  WalletCardsIcon as Cards,
} from "lucide-react";
import { useState } from "react";

interface FlashcardFormProps {
  onGenerateFlashcards: (params: FlashcardGenerationParams) => void;
  isGenerating: boolean;
  isDark?: boolean;
}

export default function FlashcardForm({
  onGenerateFlashcards,
  isGenerating,
}: FlashcardFormProps) {
  const [inputText, setInputText] = useState("");
  const [sourceLanguage, setSourceLanguage] = useState("en");
  const [targetLanguage, setTargetLanguage] = useState("hi");
  const [cardCount, setCardCount] = useState([10]);
  const [focus, setFocus] = useState("vocabulary");

  const handleSubmit = () => {
    onGenerateFlashcards({
      inputText,
      sourceLanguage,
      targetLanguage,
      cardCount: cardCount[0],
      focus,
      apiKey: "",
    });
  };

  const handleClear = () => {
    setInputText("");
  };

  return (
    <Card className="border-0 shadow-xl bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm">
      <CardHeader className="pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-violet-100 dark:bg-violet-900/30 rounded-lg">
            <BookOpen className="h-6 w-6 text-violet-600" />
          </div>
          <div>
            <CardTitle className="text-2xl">Create Your Flashcards</CardTitle>
            <CardDescription className="text-base">
              Generate multilingual flashcards with AI-powered translations
            </CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-8">
        {/* Topic Input */}
        <div className="space-y-3">
          <Label
            htmlFor="topic"
            className="text-base font-medium flex items-center gap-2"
          >
            <Cards className="h-4 w-4 text-violet-600" />
            Topic, Words, or Text
          </Label>
          <Textarea
            id="topic"
            placeholder="Enter a topic (e.g., 'travel vocabulary'), list of words, or a paragraph of text..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            className="min-h-[120px] resize-none text-base"
          />
        </div>

        <Separator />

        {/* Language Selection */}
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-3">
            <Label className="text-base font-medium flex items-center gap-2">
              <Globe className="h-4 w-4 text-violet-600" />
              Source Language
            </Label>
            <Select value={sourceLanguage} onValueChange={setSourceLanguage}>
              <SelectTrigger className="h-11">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {LANGUAGES.map((lang) => (
                  <SelectItem key={lang.code} value={lang.code}>
                    {lang.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-3">
            <Label className="text-base font-medium flex items-center gap-2">
              <Target className="h-4 w-4 text-violet-600" />
              Target Language
            </Label>
            <Select value={targetLanguage} onValueChange={setTargetLanguage}>
              <SelectTrigger className="h-11">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {LANGUAGES.map((lang) => (
                  <SelectItem key={lang.code} value={lang.code}>
                    {lang.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <Separator />

        {/* Card Count Slider */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <Label className="text-base font-medium flex items-center gap-2">
              <Cards className="h-4 w-4 text-violet-600" />
              Number of Cards
            </Label>
            <Badge variant="secondary" className="text-base px-3 py-1">
              {cardCount[0]}
            </Badge>
          </div>
          <div className="px-3">
            <Slider
              value={cardCount}
              onValueChange={setCardCount}
              max={20}
              min={5}
              step={1}
              className="w-full"
            />
            <div className="flex justify-between text-sm text-muted-foreground mt-2">
              <span>5</span>
              <span>20</span>
            </div>
          </div>
        </div>

        <Separator />

        {/* Content Focus */}
        <div className="space-y-3">
          <Label className="text-base font-medium flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-violet-600" />
            Content Focus
          </Label>
          <Select value={focus} onValueChange={setFocus}>
            <SelectTrigger className="h-11">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {CONTENT_FOCUS.map((type) => (
                <SelectItem key={type.value} value={type.value}>
                  {type.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3 pt-4">
          <Button
            variant="outline"
            onClick={handleClear}
            className="h-12 px-8"
            disabled={!inputText.trim() || isGenerating}
          >
            Clear
          </Button>
          <Button
            onClick={handleSubmit}
            className="h-12 px-8 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 flex-1"
            disabled={!inputText.trim() || isGenerating}
          >
            {isGenerating ? (
              <>
                <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4 mr-2" />
                Generate Flashcards
              </>
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
