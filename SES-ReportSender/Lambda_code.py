# 必要なライブラリをインポート
import boto3
from botocore.exceptions import ClientError

# メールを添付ファイルと共に送信する関数を定義
def send_email_with_attachment(subject, body, attachment_path):
    # boto3を使用してSESサービスのクライアントを作成、リージョンは北米東部（バージニア）に設定
    ses_client = boto3.client('ses', region_name='us-east-1')
    # メールの送信者アドレス、SESで事前に認証が必要
    sender = "sender@example.com"
    # メールの受信者アドレス
    recipient = "recipient@example.com"

    # 添付ファイルをバイナリ読み込みモードで開き、内容を読み込む
    with open(attachment_path, 'rb') as f:
        attachment = f.read()

    # メール送信を試み、エラー発生時は例外をキャッチ
    try:
        # SESを使用して生のメールデータでメールを送信
        response = ses_client.send_raw_email(
            Source=sender,
            Destinations=[recipient],
            RawMessage={
                'Data': f"""From: {sender}
To: {recipient}
Subject: {subject}
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="simple-boundary"

--simple-boundary
Content-Type: text/plain

{body}

--simple-boundary
Content-Disposition: attachment; filename="{attachment_path}"
Content-Type: application/octet-stream
Content-Transfer-Encoding: base64

{attachment.decode('utf-8')}

--simple-boundary--
"""
            }
        )
        # メール送信が成功した場合、メッセージIDを出力
        print("Email sent! Message ID:", response['MessageId'])
    except ClientError as e:
        # クライアントエラーが発生した場合、エラー情報を出力
        print("An error occurred: ", e)

# 実行例：サーバーレポートの結果をメールで送信
send_email_with_attachment("Server Report", "Attached is the server report.", "/path/to/output.txt")
