# AI Podcaster Python

AIを活用したポッドキャストスクリプト生成と音声合成ツール。

## 概要

このプロジェクトは、AIを使用してポッドキャストのスクリプトを生成し、それを音声に変換するツールです。JSONフォーマットのスクリプトテンプレートを基に、自然な会話形式のポッドキャストコンテンツを作成することができます。

## 前提条件

- Python 3.8以上
- pip（Pythonパッケージマネージャー）
- OpenAI API キー
- Google Cloud アカウントとText-to-Speech API有効化

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
├── json_script/             # JSONスクリプトテンプレートと生成
│   ├── create/             # スクリプト生成ユーティリティ
│   │   └── create_script.py  # スクリプト生成スクリプト
│   ├── aws_q_script_complete.json  # AWSに関するサンプルスクリプト
│   └── sample_script.json    # 基本的なサンプルスクリプト
├── output/                 # 生成された音声ファイルの出力先
├── text/                  # テキストファイル保存ディレクトリ
├── main.py                # メインアプリケーションエントリーポイント
├── .gitignore             # Git除外ルール
└── README.md              # プロジェクトドキュメント
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

## スクリプトフォーマット

スクリプトは以下のJSONフォーマットに従って作成します：

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

## 使用方法

1. スクリプトの準備
   - `json_script/create/create_script.py`を使用して新しいスクリプトを生成
   ```bash
   cd json_script/create
   python create_script.py
   ```
   - または`json_script/`ディレクトリに直接JSONフォーマットのスクリプトを配置

2. アプリケーションの実行
```bash
python main.py
```

3. Web インターフェース
- ローカル開発サーバー起動
```bash
python app.py
```
- アクセス
  - 開発環境: `http://localhost:5000`
  - 本番環境: `https://your-domain.com`

4. 出力確認
- 生成された音声ファイルは`output/`ディレクトリに保存
- テキストファイルは`text/`ディレクトリに保存
- Webインターフェースから音声の再生と管理が可能

## 現在の機能

- JSONフォーマットのスクリプト読み込み
- スクリプトの内容検証
- スピード調整可能なテキスト読み上げ
- 複数の話者に対応
- 出力ファイルの自動生成
- Webインターフェースによる管理

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
output/ディレクトリとtext/ディレクトリが存在することを確認してください。
必要に応じて手動で作成してください：
mkdir output
mkdir text
```

## 制限事項

- 現在サポートしている音声の言語は日本語と英語のみです
- 一度に処理できるスクリプトの長さには制限があります
- スピーカーの声質はGoogle Cloud Text-to-Speechの提供するものに限定されます

## 今後の開発予定

- より多くの言語のサポート
- カスタム音声モデルの追加
- バッチ処理機能の実装
- WebUIの機能拡張

## ライセンス

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 参考リンク

- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Google Cloud Text-to-Speech Documentation](https://cloud.google.com/text-to-speech/docs)