# ベースイメージとしてPython 3.9を使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 依存関係ファイルをコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# アプリケーションの起動コマンドを指定
CMD ["python", "app.py"]

# コンテナがリッスンするポートを指定
EXPOSE 8000
