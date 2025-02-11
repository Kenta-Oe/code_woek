import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# 環境変数からAPIキーを取得
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# APIキーが設定されていない場合のエラーハンドリング
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API キーが設定されていません。.envファイルを確認してください。")