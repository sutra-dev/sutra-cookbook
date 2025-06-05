export interface SearchResult {
  title: string;
  body: string;
  url?: string;
}

export interface SummarizeRequest {
  query: string;
  apiKey: string;
  showToolCalls: boolean;
}

export interface SummarizeResponse {
  response: string;
  error?: string;
}

export interface SearchRequest {
  query: string;
} 