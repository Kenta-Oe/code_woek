# NYT to X Bot

このボットは、New York Times（NYT）のRSSフィードから前日の記事を取得し、ChatGPTで日本語に翻訳してXに投稿するPythonスクリプトです。

## 機能

- NYTのRSSフィードから前日の記事を取得
- OpenAI GPT-4を使用して記事の要約を日本語に翻訳
- 翻訳した記事をまとめてXに投稿

## 必要要件

- Python 3.8以上
- pip（Pythonパッケージマネージャー）

## 必要なパッケージ

```bash
pip install -r requirements.txt
```

以下のパッケージが必要です：
- feedparser
- openai
- tweepy
- python-dotenv

## セットアップ手順

1. リポジトリをクローン
```bash
git clone https://github.com/Kenta-Oe/code_woek.git
cd code_woek/nyt_to_x_bot
```

2. 必要なパッケージをインストール
```bash
pip install -r requirements.txt
```

3. `.env`ファイルを作成し、以下の環境変数を設定
```
OPENAI_API_KEY=your_openai_api_key
X_API_KEY=your_x_api_key
X_API_SECRET=your_x_api_secret
X_ACCESS_TOKEN=your_x_access_token
X_ACCESS_TOKEN_SECRET=your_x_access_token_secret
```

4. 必要なAPIキーの取得
- OpenAI API キー: [OpenAIのウェブサイト](https://platform.openai.com/)から取得
- X（旧Twitter）API キー: [Xデベロッパーポータル](https://developer.twitter.com/en/portal/dashboard)から取得

## 使用方法

スクリプトを実行：
```bash
python main.py
```

## 注意事項

- OpenAI APIの利用には課金が必要です
- X APIの利用には開発者アカウントが必要です
- GPT-4モデルを使用するため、OpenAIのGPT-4アクセス権限が必要です

## ファイル構成

- `main.py`: メインのスクリプトファイル
- `config.py`: 設定ファイル（APIキーなどの環境変数を管理）
- `.env`: 環境変数ファイル（手動で作成必要）

## LICENSE

MIT