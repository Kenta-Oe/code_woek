import jwt

# 任意のJWTシークレットキー
jwt_secret = 'lkjhhgfdg'


# エンコードされた検証するトークン
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEsImV4cCI6MTcxMTYzODYxOX0.6GzMhs9oJ7BKsCmN1N9zym96EWU1DYUoMuTGc4T1KTY'

try:
    # JWTトークンの検証
    decoded = jwt.decode(token, jwt_secret, algorithms=['HS256'])
    print(decoded)
except jwt.ExpiredSignatureError:
    print('トークンの有効期限が切れています。')
except jwt.InvalidTokenError:
    print('無効なトークンです。')


### 正規の出力例
### {'userId': 1, 'exp': 1711638619}