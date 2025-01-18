# AWS News Summary Generator

AWSに関連するニュースをRSSフィードから取得し、サービスごとにExcelファイルにまとめるツールです。

## 機能

- 複数のRSSフィードからAWS関連ニュースを取得
  - AWS 公式の新着情報（What's New）
  - Developers.IO のAWS関連記事
  - AWS Machine Learning ブログ
  - AWS 日本語ブログ
- サービスごとにカテゴリ分類
- GPT-4による記事要約
- 記事の重複取得を防止
- サービスごとにExcelファイルへの自動出力
- 30日以上前の古い記事履歴の自動クリーンアップ
- 処理結果の詳細なログ表示

## 必要な環境変数

`.env`ファイルに以下の環境変数を設定してください：

```
OPENAI_API_KEY=your_openai_api_key
AWS_NEWS_RSS=https://aws.amazon.com/jp/about-aws/whats-new/recent/feed/
DEVELOPERS_IO_RSS=https://developers.io/category/aws/feed/
AWS_ML_BLOG_RSS=https://aws.amazon.com/blogs/machine-learning/feed/
AWS_JP_BLOG_RSS=https://aws.amazon.com/jp/blogs/news/feed/
```

## 使用方法

1. 必要なパッケージをインストール：
   ```bash
   pip install -r requirements.txt
   ```

2. `.env`ファイルを作成し、必要な環境変数を設定

3. スクリプトを実行：
   ```bash
   python main.py
   ```

4. デスクトップの`aws_news_summary`フォルダに結果が出力されます

## 出力形式

- サービスごとにフォルダが作成されます
- 各フォルダ内にExcelファイルが生成されます
- Excelファイルには以下の情報が含まれます：
  - 日付
  - タイトル
  - 要約
  - 記事リンク

## ログ出力

- 取得開始時に読み込まれたサービス数を表示
- 各RSSフィードごとの処理状況を表示
  - フィード内の総記事数
  - 新規に取得された記事数
  - スキップされた記事数（重複）
- 最後に全体の新規記事数を表示

## 処理の流れ

1. 環境変数とサービスリストの読み込み
2. 古い記事履歴のクリーンアップ（30日以上前）
3. 各RSSフィードに対して：
   - フィードの取得と解析
   - 各記事に対して：
     - 重複チェック
     - サービス名の検出
     - 要約生成（GPT-4使用）
     - Excelファイルへの保存
4. 処理結果のサマリー表示

## 更新履歴

### 2024-01-18
- 複数のRSSフィードに対応
  - Developers.IO
  - AWS Machine Learning ブログ
  - AWS 日本語ブログ
  を追加
- フィードごとの処理結果の詳細表示を追加
- 記事取得時のエラーハンドリングを強化