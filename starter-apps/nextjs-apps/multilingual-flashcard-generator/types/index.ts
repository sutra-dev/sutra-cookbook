export interface Flashcard {
  id: string;
  front: string;
  back: string;
  example?: string;
}

export interface Language {
  code: string;
  name: string;
}

export interface ContentFocusOption {
  value: string;
  label: string;
}

export interface FlashcardGenerationParams {
  inputText: string;
  sourceLanguage: string;
  targetLanguage: string;
  cardCount: number;
  focus: string;
  apiKey: string;
}
