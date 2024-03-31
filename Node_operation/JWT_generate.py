import jwt
import datetime

# JWTシークレットキー
jwt_secret = 'your_secret_key'

# ペイロードデータ
payload = {
    'userId': 1,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 有効期限を1時間後に設定
}

# JWTトークンの生成
token = jwt.encode(payload, jwt_secret, algorithm='HS256')

print(token)
