import os
from api_config import OPENAI_API_KEY

# Flask 設定
SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

# OpenAI 設定
MODEL_NAME = "o1-mini"

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