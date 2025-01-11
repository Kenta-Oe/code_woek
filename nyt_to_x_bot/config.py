import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# NYT RSS設定
NYT_RSS_URL = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")