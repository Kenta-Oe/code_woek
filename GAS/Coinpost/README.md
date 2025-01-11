# Coinpost Article Summarizer

このプロジェクトは、Google Apps Script (GAS)を使用して、Coinpostの記事を自動的に取得、要約し、Xに投稿するボットです。

## 機能

- Coinpostの前日の記事を自動取得
- ChatGPTを使用して記事の要約を作成
- 要約をGoogle Driveに保存
- Xに自動投稿する機能

## セットアップ手順

1. Google Apps Scriptプロジェクトを作成
   - [Google Apps Script](https://script.google.com/) にアクセス
   - 新しいプロジェクトを作成

2. 必要なファイルをアップロード
   - `Main.gs`をプロジェクトにコピー
   - その他必要なスクリプトファイルを追加

3. プロジェクトの設定
   - スクリプトプロパティに以下の値を設定：
     - `X_API_KEY`: XのAPI Key
     - `X_API_SECRET`: XのAPI Secret
     - `X_ACCESS_TOKEN`: Xのアクセストークン
     - `X_ACCESS_TOKEN_SECRET`: Xのアクセストークンシークレット
     - `OPENAI_API_KEY`: OpenAIのAPIキー

4. Google Driveの設定
   - 保存先フォルダを作成
   - フォルダIDを`Main.gs`の`folderId`変数に設定

## トリガーの設定

1. Apps Scriptのトリガー設定画面を開く
2. 新しいトリガーを追加
   - 実行する関数: `fetchAndSummarizeCoinPostArticles`
   - イベントのソース: `時間主導型`
   - 時間ベースのトリガーのタイプ: `日付ベースのタイマー`
   - 時刻: 必要な時間を設定（例：毎日午前9時）

## 注意事項

- OpenAI APIの利用には課金が必要です
- X APIの利用には開発者アカウントが必要です
- Google Apps Scriptの実行時間制限（6分）に注意してください

## ファイル構成

- `Main.gs`: メインの実行ファイル
  - 記事の取得
  - 要約の作成
  - Drive保存
  - X投稿の機能を含む

## エラーハンドリング

スクリプトは以下の状況でエラーログを出力します：
- 記事が取得できない場合
- Drive保存に失敗した場合
- X投稿に失敗した場合

## LICENSE

MIT