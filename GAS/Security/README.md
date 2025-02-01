# セキュリティニュース自動要約・投稿システム

このプロジェクトは、セキュリティ関連のニュースを自動で収集し、要約して保存・共有するGoogle Apps Script（GAS）プログラムです。

## 🌟 主な機能

1. RSSフィードからニュース記事を取得
2. AIによる記事の要約生成
3. 要約したコンテンツのGoogle Driveへの保存
4. Xへの自動投稿

## 📁 ファイル構成

- `Main.gs`: メインの実行ファイル。全体の処理フローを制御
- `SecurityNews.gs`: RSSフィードからニュース記事を取得
- `ChatGPT.gs`: OpenAIのAPIを使用して記事を要約
- `Post.gs`: X（旧Twitter）への投稿を処理

## 🚀 セットアップ方法

### 1. 必要なAPIキーの準備

#### OpenAI APIキー
1. [OpenAIのウェブサイト](https://platform.openai.com/)でアカウントを作成
2. APIキーを取得

#### X（Twitter）APIキー
1. [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)でアカウントを作成
2. 以下の4つのキーを取得：
   - API Key (consumer key)
   - API Secret (consumer secret)
   - Access Token
   - Access Token Secret

### 2. GASプロジェクトの設定

1. [Google Apps Script](https://script.google.com/)で新規プロジェクトを作成
2. 各`.gs`ファイルをプロジェクトにコピー
3. スクリプトプロパティに以下を設定：
   - `OPENAI_API_KEY`: OpenAIのAPIキー
   - `X_API_KEY`: X（Twitter）のAPI Key
   - `X_API_SECRET`: X（Twitter）のAPI Secret
   - `X_ACCESS_TOKEN`: X（Twitter）のAccess Token
   - `X_ACCESS_TOKEN_SECRET`: X（Twitter）のAccess Token Secret

### 3. Google Driveの設定

1. 要約ファイルを保存するフォルダをGoogle Driveに作成
2. フォルダのIDを`Main.gs`の`YOUR_SECURITY_FOLDER_ID`に設定

## ⚙️ 使用方法

1. `fetchAndSummarizeSecurityArticles()`関数を実行すると：
   - RSSフィードから最新の記事を取得
   - 各記事をAIで要約
   - 要約をGoogle Driveに保存
   - Xに投稿

2. 定期実行する場合：
   - GASのトリガーを設定（例：1日1回）
   - `fetchAndSummarizeSecurityArticles`関数を指定

## 🔧 カスタマイズ

### RSSフィードの変更
`SecurityNews.gs`の`url`変数を変更することで、別のRSSフィードに変更できます：
```javascript
const url = 'YOUR_RSS_FEED_URL';
```

### 要約の調整
`ChatGPT.gs`の`promptText`を編集することで、要約の長さや形式を変更できます。

## ⚠️ 注意事項

- APIの利用制限に注意してください
- X投稿の文字数制限（280文字）を考慮してください
- 要約の品質は入力となる記事の質に依存します
- OpenAIのAPIには課金が発生する可能性があります

## 🤝 貢献方法

1. このリポジトリをフォーク
2. 新しいブランチを作成
3. 変更を加えてコミット
4. プルリクエストを作成

## 📝 ライセンス

MITライセンスで公開しています。