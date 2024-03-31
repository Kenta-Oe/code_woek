import jwt
import sys

# コマンドライン引数からトークンを取得
if len(sys.argv) != 2:
    print("使用方法: python script.py [JWTトークン]")
    sys.exit(1)

token = sys.argv[1]

# 秘密鍵を外部ファイルから読み込む
secret_file = '/Users/ooekenfutoshi/Desktop/Python/Node_operation/seacret_fail.txt'
try:
    with open(secret_file, 'r') as file:
        jwt_secret = file.read().strip()
except FileNotFoundError:
    print(f"秘密鍵ファイルが見つかりません: {secret_file}")
    sys.exit(1)

# JWTトークンの検証
try:
    decoded = jwt.decode(token, jwt_secret, algorithms=['HS256'])
    print("デコードされたトークン:", decoded)
except jwt.ExpiredSignatureError:
    print('トークンの有効期限が切れています。')
except jwt.InvalidTokenError:
    print('無効なトークンです。')
