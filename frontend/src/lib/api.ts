const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

export interface Word {
  _id: string;
  english: string;
  chinese: string;
  phonetic: string;
  pos: string;
  level: number;
  frequency: number;
  examples: string[];
  tags: string[];
}

export async function getAllWords(): Promise<Word[]> {
  const response = await fetch(`${API_BASE_URL}/words`);
  if (!response.ok) {
    throw new Error('Failed to fetch words');
  }
  return response.json();
}

export async function getWordsByLevel(level: number): Promise<Word[]> {
  const response = await fetch(`${API_BASE_URL}/words/level/${level}`);
  if (!response.ok) {
    throw new Error('Failed to fetch words by level');
  }
  return response.json();
}

export async function searchWords(query: string): Promise<Word[]> {
  const response = await fetch(`${API_BASE_URL}/words/search?query=${encodeURIComponent(query)}`);
  if (!response.ok) {
    throw new Error('Failed to search words');
  }
  return response.json();
} 