## プロジェクト構造

```
ai-podcaster_python/
├── json_script/             # JSONスクリプトテンプレートと生成
│   ├── create/             # スクリプト生成ユーティリティ
│   │   └── create_script.py  # スクリプト生成ツール
│   ├── aws_q_script_complete.json  # AWSクイズのサンプルスクリプト
│   └── sample_script.json    # 基本的なサンプルスクリプト
├── output/                 # 生成された音声ファイルの出力先
│   └── *.mp3              # 生成された音声ファイル
├── text/                  # テキストファイル保存ディレクトリ
│   └── *.txt              # 生成されたテキストファイル
├── main.py                # メインアプリケーションエントリーポイント
├── .gitignore             # Git除外設定ファイル
└── README.md              # プロジェクトドキュメント
```