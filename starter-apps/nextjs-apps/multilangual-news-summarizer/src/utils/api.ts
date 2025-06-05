import { SearchResult, SummarizeRequest, SummarizeResponse } from '@/types';

/**
 * Search for recent information using DuckDuckGo
 */
export async function searchDuckDuckGo(query: string): Promise<SearchResult[]> {
  try {
    const response = await fetch('/api/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to get search results');
    }

    return await response.json();
  } catch (error: any) {
    console.error('Error searching DuckDuckGo:', error);
    throw new Error(`Search failed: ${error.message}`);
  }
}

/**
 * Generate a summary using the Sutra API
 */
export async function generateSummary(
  params: SummarizeRequest
): Promise<string> {
  try {
    const { query, apiKey, showToolCalls } = params;
    
    const response = await fetch('/api/summarize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, apiKey, showToolCalls }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to generate summary');
    }

    const data: SummarizeResponse = await response.json();
    return data.response;
  } catch (error: any) {
    console.error('Error generating summary:', error);
    throw new Error(`Summary generation failed: ${error.message}`);
  }
}

/**
 * Add current date information to query
 */
export function addDateToQuery(query: string): string {
  const currentDate = new Date().toISOString().split('T')[0];
  return `${query}\n\nToday's date is ${currentDate}. Please provide the most up-to-date information available.`;
} 