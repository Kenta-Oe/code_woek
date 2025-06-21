// Amazon ブランドカラー
export const COLORS = {
  primary: '#FF9900', // Amazon Orange
  secondary: '#232F3E', // Amazon Dark Blue
  accent: '#146EB4', // Amazon Blue
  background: '#FFFFFF',
  text: '#0F1111',
  textSecondary: '#565959',
  border: '#D5D9D9',
  success: '#007600',
  error: '#C40000',
  warning: '#FF9900',
} as const;

// ナビゲーションカテゴリー
export const NAV_CATEGORIES = [
  'すべて',
  '今日のセール',
  'Prime',
  'カスタマーサービス',
  'レジストリ',
  'ギフトカード',
  'セール',
  '新着商品',
] as const;

// 商品カテゴリー
export const PRODUCT_CATEGORIES = [
  'エレクトロニクス',
  'コンピュータ',
  'スマートフォン',
  '本',
  '映画・音楽・ゲーム',
  'ホーム・キッチン',
  'スポーツ・アウトドア',
  'ファッション',
  'ビューティー',
  'おもちゃ',
  '自動車',
  'ヘルスケア',
  'ペット用品',
  'ベビー用品',
  'オフィス用品',
] as const;

// フッターリンク
export const FOOTER_LINKS = {
  'Amazonについて': [
    'Amazonについて',
    '採用情報',
    'プレスリリース',
    'Amazonのブログ',
    '投資家向け情報',
  ],
  'お金を稼ぐ': [
    '商品を出品',
    'パートナーになる',
    'アソシエイトになる',
    '広告を出す',
    'Kindle本を出版',
  ],
  '支払い方法': [
    'Amazonポイント',
    'Amazonギフトカード',
    'Amazonマスターカード',
    '分割払い',
  ],
  'ヘルプ': [
    'Amazonでヘルプ',
    '配送・返品・交換',
    'コンテンツとデバイス',
    'アプリのダウンロード',
    'カスタマーサービス',
  ],
} as const; 