# AI Podcaster Python

AIを活用したポッドキャストスクリプト生成と音声合成ツール。

## 概要

このプロジェクトは、AIを使用してポッドキャストのスクリプトを生成し、それを音声に変換するツールです。JSONフォーマットのスクリプトテンプレートを基に、自然な会話形式のポッドキャストコンテンツを作成することができます。

## 前提条件

- Python 3.8以上
- pip（Pythonパッケージマネージャー）

## 必要なパッケージ

```bash
pip install -r requirements.txt
```

以下のパッケージが必要です：
- python-dotenv
- openai
- google-cloud-texttospeech
- pydub

## プロジェクト構造

```
ai-podcaster_python/
├── json_script/         # JSONスクリプトテンプレートと生成
│   ├── create/         # スクリプト作成ユーティリティ
│   └── sample_script.json   # サンプルスクリプトフォーマット
├── main.py             # メインアプリケーションエントリーポイント
├── requirements.txt    # 依存パッケージリスト
├── .env               # 環境変数（git管理外）
├── .gitignore         # Git除外ルール
└── README.md          # プロジェクトドキュメント
```

## セットアップ手順

1. リポジトリのクローン
```bash
git clone https://github.com/Kenta-Oe/code_woek.git
cd ai-podcaster_python
```

2. 環境変数の設定
`.env`ファイルを作成し、以下の環境変数を設定：
```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
```

3. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

4. Google Cloud認証情報の設定
- Google Cloud Consoleでプロジェクトを作成
- Text-to-Speech APIを有効化
- サービスアカウントキーを生成し、プロジェクトルートに配置

## 使用方法

1. スクリプトテンプレートの準備
   - `json_script/`ディレクトリにJSONフォーマットのスクリプトを配置
   - 以下のフォーマットに従ってスクリプトを作成

2. スクリプトのフォーマット
```json
{
    "title": "サンプルタイトル",
    "description": "スクリプトの説明",
    "reference": "参照元",
    "script": [
        {
            "text": "ナレーションテキスト",
            "speaker": "ナレーター",
            "speed": 1.0
        }
    ]
}
```

3. アプリケーションの実行
```bash
python main.py
```

4. 出力
- 生成された音声ファイルは`output/`ディレクトリに保存されます
- 各音声ファイルは`{タイトル}_{タイムスタンプ}.mp3`の形式で保存されます

## エラー対処

よくあるエラーと解決方法：

1. API認証エラー
```
環境変数が正しく設定されているか確認してください。
特にOPENAI_API_KEYとGOOGLE_APPLICATION_CREDENTIALSの設定を確認してください。
```

2. スクリプトフォーマットエラー
```
JSONファイルの構文が正しいか確認してください。
必須フィールド（title, script）が含まれているか確認してください。
```

3. 出力ディレクトリエラー
```
output/ディレクトリが存在することを確認してください。
必要に応じて手動で作成してください：mkdir output
```

## 制限事項

- 現在サポートしている音声の言語は日本語と英語のみです
- 一度に処理できるスクリプトの長さには制限があります
- スピーカーの声質はGoogle Cloud Text-to-Speechの提供するものに限定されます

## ライセンス

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 参考リンク

- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Google Cloud Text-to-Speech Documentation](https://cloud.google.com/text-to-speech/docs)