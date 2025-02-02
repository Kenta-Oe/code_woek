# NYT記事翻訳・投稿システム

このプロジェクトは、New York Timesの記事を自動で取得し、日本語に翻訳して保存・共有するGoogle Apps Script（GAS）プログラムです。

## 🌟 主な機能

1. NYT RSSフィードからの記事取得
2. AIによる英日翻訳
3. 翻訳したコンテンツのGoogle Driveへの保存
4. Xへの自動投稿
5. 指定メールアドレスへの翻訳結果送信

## 📁 ファイル構成

- `Main.gs`: メインの実行ファイル。全体の処理フローを制御
- `NYTNews.gs`: NYTのRSSフィードから記事を取得
- `ChatGPT.gs`: OpenAIのAPIを使用して記事を翻訳
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

1. 翻訳記事を保存するフォルダをGoogle Driveに作成
2. フォルダのIDを`Main.gs`の`YOUR_NYT_FOLDER_ID`に設定

### 4. メール通知の設定

1. `Main.gs`の`sendSummaryEmail`関数で送信先メールアドレスを設定
2. 必要に応じて件名や送信者名をカスタマイズ

## ⚙️ 使用方法

1. `fetchAndTranslateNYTArticles()`関数を実行すると：
   - NYTのRSSフィードから最新の記事を取得
   - ChatGPTで日本語に翻訳
   - 翻訳結果をGoogle Driveに保存
   - Xに投稿
   - 指定メールアドレスに翻訳を送信

2. 定期実行する場合：
   - GASのトリガーを設定（例：1日1回）
   - `fetchAndTranslateNYTArticles`関数を指定

## 🔧 カスタマイズ

### RSSフィードの変更
`NYTNews.gs`の`url`変数を変更することで、別のRSSフィードに変更できます：
```javascript
const url = 'YOUR_RSS_FEED_URL';
```

### 翻訳の調整
`ChatGPT.gs`の`promptText`を編集することで、翻訳のスタイルを変更できます。

### メール通知の調整
`Main.gs`の`sendSummaryEmail`関数で以下をカスタマイズできます：
- 送信先メールアドレス
- メールの件名フォーマット
- 送信者名
- メール本文のフォーマット

## ⚠️ 注意事項

- APIの利用制限に注意してください
- X投稿の文字数制限（280文字）を考慮してください
- 翻訳の品質は入力となる記事の質に依存します
- OpenAIのAPIには課金が発生する可能性があります
- Gmail APIの制限に注意してください
- NYTのRSSフィードの利用規約を確認してください

## 🤝 貢献方法

1. このリポジトリをフォーク
2. 新しいブランチを作成
3. 変更を加えてコミット
4. プルリクエストを作成

## 📝 ライセンス

MITライセンスで公開しています。