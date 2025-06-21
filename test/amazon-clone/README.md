# Amazonクローン

Amazonの主要なUI機能を再現したWebアプリケーションです。

## 機能

- 🛍️ **商品表示**: 商品カード、評価、価格表示
- 🔍 **検索機能**: 商品検索バー
- 📱 **レスポンシブデザイン**: モバイル・タブレット・デスクトップ対応
- 🎨 **Amazonスタイル**: 本家Amazonに近いデザイン
- ⭐ **評価システム**: 星評価とレビュー数表示
- 🏷️ **カテゴリー分類**: 商品カテゴリー表示
- 🎯 **特価商品**: セール商品の表示
- 🚀 **Prime商品**: Prime対象商品の表示

## 技術スタック

- **フレームワーク**: Next.js 15.3.4
- **言語**: TypeScript
- **スタイリング**: Tailwind CSS 4
- **React**: 19.0.0

## プロジェクト構造

```
src/
├── app/
│   ├── layout.tsx          # ルートレイアウト
│   ├── page.tsx            # メインページ
│   └── globals.css         # グローバルスタイル
├── components/
│   ├── layout/
│   │   ├── Header.tsx      # ヘッダーコンポーネント
│   │   ├── Footer.tsx      # フッターコンポーネント
│   │   └── Layout.tsx      # レイアウトコンポーネント
│   ├── ui/
│   │   ├── SearchBar.tsx   # 検索バー
│   │   ├── ProductCard.tsx # 商品カード
│   │   ├── CategoryCard.tsx # カテゴリーカード
│   │   ├── HeroBanner.tsx  # ヒーローバナー
│   │   └── ProductGrid.tsx # 商品グリッド
│   └── pages/
│       └── HomePage.tsx    # ホームページ
├── types/
│   └── index.ts            # 型定義
└── utils/
    └── constants.ts        # 定数
```

## コンポーネント説明

### レイアウトコンポーネント
- **Header**: Amazonスタイルのヘッダー（ロゴ、検索バー、ナビゲーション）
- **Footer**: フッター（リンク、ソーシャルメディア）
- **Layout**: 全体レイアウトの管理

### UIコンポーネント
- **SearchBar**: カテゴリー選択付き検索バー
- **ProductCard**: 商品情報表示カード（画像、価格、評価、Prime表示）
- **CategoryCard**: カテゴリー表示カード
- **HeroBanner**: メインバナー（セール情報など）
- **ProductGrid**: 商品グリッド表示

## 開始方法

### 前提条件
- Node.js 18.0.0以上
- npm または yarn

### インストール

```bash
# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run dev
```

### ビルド

```bash
# プロダクションビルド
npm run build

# プロダクションサーバーの起動
npm start
```

## 開発ガイド

### 新しいコンポーネントの追加
1. `src/components/ui/` または `src/components/layout/` に新しいコンポーネントファイルを作成
2. TypeScript型定義を `src/types/index.ts` に追加
3. 必要に応じて定数を `src/utils/constants.ts` に追加

### スタイリング
- Tailwind CSSを使用
- Amazonのブランドカラーは `src/utils/constants.ts` で定義
- レスポンシブデザインを心がける

### 型安全性
- すべてのコンポーネントでTypeScript型定義を使用
- インターフェースは `src/types/index.ts` で管理

## 今後の実装予定

- [ ] 商品詳細ページ
- [ ] カート機能
- [ ] ユーザー認証
- [ ] 商品レビュー機能
- [ ] お気に入り機能
- [ ] フィルタリング・ソート機能
- [ ] 決済システム

## ライセンス

このプロジェクトは学習目的で作成されています。Amazonの商標はAmazon.com, Inc.に帰属します。

## 貢献

プルリクエストやイシューの報告を歓迎します。大きな変更を行う場合は、まずイシューで議論してください。
