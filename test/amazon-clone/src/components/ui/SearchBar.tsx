'use client';

import { useState } from 'react';
import { COLORS } from '@/utils/constants';

interface SearchBarProps {
  onSearch?: (query: string) => void;
  placeholder?: string;
  className?: string;
}

export default function SearchBar({ 
  onSearch, 
  placeholder = "Amazon.co.jp で検索", 
  className = "" 
}: SearchBarProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (onSearch && query.trim()) {
      onSearch(query.trim());
    }
  };

  return (
    <form 
      onSubmit={handleSubmit}
      className={`flex flex-1 max-w-2xl ${className}`}
    >
      <div className="relative flex w-full">
        {/* カテゴリードロップダウン */}
        <select 
          className="bg-gray-100 border border-gray-300 text-gray-700 py-2 px-3 rounded-l-md border-r-0 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
          style={{ backgroundColor: '#f3f3f3' }}
        >
          <option value="">すべて</option>
          <option value="electronics">エレクトロニクス</option>
          <option value="books">本</option>
          <option value="fashion">ファッション</option>
          <option value="home">ホーム・キッチン</option>
        </select>

        {/* 検索入力フィールド */}
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          className="flex-1 px-4 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
        />

        {/* 検索ボタン */}
        <button
          type="submit"
          className="px-6 py-2 bg-orange-500 text-white rounded-r-md hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 transition-colors"
          style={{ backgroundColor: COLORS.primary }}
        >
          <svg 
            className="w-5 h-5" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" 
            />
          </svg>
        </button>
      </div>
    </form>
  );
} 