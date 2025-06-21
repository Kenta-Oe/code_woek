'use client';

import { useState } from 'react';
import SearchBar from '../ui/SearchBar';
import { COLORS } from '@/utils/constants';

export default function Header() {
  const [cartCount, setCartCount] = useState(0);

  const handleSearch = (query: string) => {
    console.log('検索クエリ:', query);
    // 検索機能の実装
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      {/* 上部ナビゲーション */}
      <div className="bg-gray-800 text-white py-1 px-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between text-xs">
          <div className="flex items-center space-x-4">
            <span>Amazon.co.jp</span>
            <span>|</span>
            <span>配送先: 日本</span>
          </div>
          <div className="flex items-center space-x-4">
            <a href="#" className="hover:text-orange-400">アカウント & リスト</a>
            <a href="#" className="hover:text-orange-400">注文履歴</a>
            <a href="#" className="hover:text-orange-400">カスタマーサービス</a>
          </div>
        </div>
      </div>

      {/* メインヘッダー */}
      <div className="max-w-7xl mx-auto px-4 py-3">
        <div className="flex items-center space-x-4">
          {/* Amazonロゴ */}
          <div className="flex-shrink-0">
            <a href="/" className="text-2xl font-bold text-gray-900">
              <span style={{ color: COLORS.primary }}>Amazon</span>
            </a>
          </div>

          {/* 検索バー */}
          <div className="flex-1 max-w-2xl">
            <SearchBar onSearch={handleSearch} />
          </div>

          {/* 右側のナビゲーション */}
          <div className="flex items-center space-x-6">
            {/* アカウント */}
            <div className="text-sm">
              <div className="text-gray-500">こんにちは、サインイン</div>
              <div className="font-medium">アカウント & リスト</div>
            </div>

            {/* 注文履歴 */}
            <div className="text-sm">
              <div className="text-gray-500">返品</div>
              <div className="font-medium">& 注文</div>
            </div>

            {/* カート */}
            <div className="relative">
              <button className="flex items-center space-x-1 text-sm">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m6-5v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m8 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4.01" />
                </svg>
                <span>カート</span>
                {cartCount > 0 && (
                  <span className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {cartCount}
                  </span>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* 下部ナビゲーション */}
      <div className="bg-gray-100 border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4">
          <nav className="flex items-center space-x-6 py-2 text-sm">
            <button className="flex items-center space-x-1 hover:text-orange-600">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <span>すべて</span>
            </button>
            <a href="#" className="hover:text-orange-600">今日のセール</a>
            <a href="#" className="hover:text-orange-600">Prime</a>
            <a href="#" className="hover:text-orange-600">カスタマーサービス</a>
            <a href="#" className="hover:text-orange-600">レジストリ</a>
            <a href="#" className="hover:text-orange-600">ギフトカード</a>
            <a href="#" className="hover:text-orange-600">セール</a>
            <a href="#" className="hover:text-orange-600">新着商品</a>
          </nav>
        </div>
      </div>
    </header>
  );
} 