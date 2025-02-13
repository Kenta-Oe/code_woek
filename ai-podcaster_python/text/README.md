# AI Podcaster

AIを活用したポッドキャスト台本生成・音声生成システム

## 機能

- テキストとURLから自動でポッドキャスト台本を生成
- 生成された台本の要約作成
- 台本からMP3音声ファイルの生成
- JSONフォーマットでの台本エクスポート
- 生成履歴の管理

## セットアップ

### 必要条件

- Python 3.8以上
- OpenAI API キー
- Flask

### インストール

1. リポジトリをクローン
```bash
git clone https://github.com/Kenta-Oe/code_woek.git
cd ai-podcaster_python/text
```

2. 必要なパッケージをインストール
```bash
pip install -r requirements.txt
```

3. 環境変数の設定
`.env`ファイルを作成し、以下の内容を設定：
```
OPENAI_API_KEY=your_openai_api_key_here
FLASK_SECRET_KEY=your_flask_secret_key
```

## 使い方

1. サーバーの起動
```bash
python app.py
```

2. ブラウザで以下のURLにアクセス
```
http://localhost:5000
```

3. フォームに以下の情報を入力
- 参考情報（台本のベースとなるテキスト）
- 参考URL（関連する情報源のURL）

4. 必要な機能を選択
- 「台本生成」: AIによる台本の生成
- 「要約生成」: 生成された台本の要約
- 「JSON生成」: 台本のJSON形式でのエクスポート
- 「MP3生成」: 音声ファイルの生成

## ディレクトリ構造

```
text/
├── .env                # 環境変数設定
├── api_config.py       # API設定
├── app.py             # メインアプリケーション
├── config.py          # 設定ファイル
├── static/            # 静的ファイル
└── templates/         # HTMLテンプレート
```

## ライセンス

MIT License

## 注意事項

- APIキーは必ず`.env`ファイルで管理し、公開リポジトリにコミットしないでください
- 生成された台本の著作権や利用規約については、OpenAIのガイドラインに従ってください