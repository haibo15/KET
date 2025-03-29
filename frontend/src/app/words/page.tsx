'use client';

import { useState, useEffect } from 'react';
import Layout from '@/components/layout/Layout';
import WordList from '@/components/words/WordList';
import SearchBar from '@/components/words/SearchBar';
import { getAllWords, searchWords, Word } from '@/lib/api';

export default function WordsPage() {
  const [words, setWords] = useState<Word[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadWords();
  }, []);

  const loadWords = async () => {
    try {
      setLoading(true);
      const data = await getAllWords();
      setWords(data);
      setError(null);
    } catch (error) {
      console.error('加载单词失败:', error);
      setError('加载单词失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadWords();
      return;
    }

    try {
      setLoading(true);
      const data = await searchWords(searchQuery);
      setWords(data);
      setError(null);
    } catch (error) {
      console.error('搜索失败:', error);
      setError('搜索失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  const handlePlayWord = (word: Word) => {
    // TODO: 实现单词发音功能
    console.log('播放单词:', word.english);
  };

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-800">词汇学习</h1>
          <div className="w-1/2">
            <SearchBar
              value={searchQuery}
              onChange={setSearchQuery}
              onSubmit={handleSearch}
            />
          </div>
        </div>

        {loading && (
          <div className="text-center py-8">
            <p className="text-gray-600">加载中...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {!loading && !error && words.length === 0 && (
          <div className="text-center py-8">
            <p className="text-gray-600">没有找到相关单词</p>
          </div>
        )}

        {!loading && !error && words.length > 0 && (
          <WordList words={words} onPlayWord={handlePlayWord} />
        )}
      </div>
    </Layout>
  );
} 