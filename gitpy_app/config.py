import os
import secrets

class Config:
    # アプリケーションの設定
    SECRET_KEY = secrets.token_hex(16)
    
    # ファイルアップロード設定
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大16MB
    
    # リポジトリのベースディレクトリ
    REPO_BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'repositories')
    
    # デバッグモード（開発環境では True、本番環境では False）
    DEBUG = True