# AWS News Tracker

AWSの新着ニュースを自動で収集し、GPT-4で要約してExcelファイルに整理するPythonスクリプト

## 機能

- AWS What's Newのフィードから最新ニュースを自動取得
- GPT-4を使用して記事内容を簡潔に要約
- AWSサービスごとにExcelファイルを作成して整理
- 既に処理済みの記事を管理し重複を防止
- 30日以上経過した古い記事履歴の自動クリーンアップ

## セットアップ

1. リポジトリをクローン:
```bash
git clone https://github.com/Kenta-Oe/code_woek.git
cd code_woek/my_aws_news
```

2. 必要なパッケージをインストール:
```bash
pip install -r requirements.txt
```

3. `.env`ファイルを作成し、以下の環境変数を設定:
```
OPENAI_API_KEY=your_openai_api_key
AWS_NEWS_RSS=https://aws.amazon.com/jp/about-aws/whats-new/recent/feed/
```

## 使用方法

スクリプトを実行:
```bash
python main.py
```

実行すると以下の処理が行われます:
- AWSの新着ニュースフィードを取得
- 記事タイトルからAWSサービスを判別
- GPT-4で記事内容を要約
- サービスごとのExcelファイルに記事情報を保存

## ファイル構成

- `main.py`: メインスクリプト
- `article_manager.py`: 記事の処理状態を管理するクラス
- `service_classifier.py`: AWSサービス名を判別する機能
- `service_list.txt`: AWSサービス名のリスト
- `requirements.txt`: 必要なPythonパッケージ
- `.gitignore`: Git管理から除外するファイル設定

## 出力ファイル

デフォルトでは`~/OneDrive/デスクトップ/aws_news_summary/`以下に以下のような構造で出力されます:
```
aws_news_summary/
├── Amazon EC2/
│   └── Amazon EC2.xlsx
├── Amazon S3/
│   └── Amazon S3.xlsx
├── Other/
│   └── Other.xlsx
└── processed_articles.json
```

各Excelファイルには以下の情報が含まれます:
- 日付
- タイトル
- 要約
- リンク

## 依存パッケージ

- feedparser==6.0.10
- openai==1.3.0
- requests==2.31.0
- python-dotenv==1.0.0
- openpyxl==3.1.2

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。