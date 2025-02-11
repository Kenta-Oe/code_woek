import os
from dotenv import load_dotenv
from api_config import OPENAI_API_KEY

# .envファイルを読み込む
load_dotenv()

# OpenAI 設定
MODEL_NAME = "gpt-3.5-turbo"  # 最新のモデルに更新

# Flask 設定
SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

# ディレクトリパス設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
JSON_OUTPUT_DIR = os.path.join(BASE_DIR, "..", "json_script")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# ファイルパス設定
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# 必要なディレクトリの作成
for directory in [OUTPUT_DIR, JSON_OUTPUT_DIR, LOG_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)