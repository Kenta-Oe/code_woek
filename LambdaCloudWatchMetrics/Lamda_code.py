
import json
import boto3  #AWSサービスと対話するためのPython SDK


def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Lambda関数のメインハンドラーを定義します。Lambdaはこの関数をエントリーポイントとして使用します
def lambda_handler(event, context):
    # boto3を使用してCloudWatchサービスとやり取りするためのCloudWatchクライアントを作成します
    cloudwatch = boto3.client('cloudwatch')
    
    # S3に保存されたJSONファイルからインスタンスの設定を読み込み、'instances'セクションにアクセスします
    instances = load_config('/path/to/instances.json')['instances']
    
    # S3に保存されたJSONファイルからメトリクスの設定を読み込み、'metrics'セクションにアクセスします
    metrics = load_config('/path/to/metrics.json')['metrics']
    
    # CloudWatchからの結果を格納するための空のリストを初期化します
    results = []

    # 設定ファイルで指定された各インスタンスに対してループ処理を行います
    for instance in instances:
        # 設定ファイルで指定された各メトリクスに対してループ処理を行います
        for metric in metrics:
            # 現在のインスタンスとメトリクスに対してCloudWatchからメトリクス統計を取得します
            response = cloudwatch.get_metric_statistics(
                Namespace=metric['Namespace'],                     # メトリクスが属する名前空間
                MetricName=metric['MetricName'],                   # メトリクスの名前
                Dimensions=[{'Name': 'InstanceId', 'Value': instance['InstanceId']}],  # インスタンスに基づく寸法
                StartTime=datetime.utcnow() - timedelta(hours=1),  # 開始時間（1時間前）
                EndTime=datetime.utcnow(),                         # 終了時間（現在時刻）
                Period=metric['Period'],                           # データを集計する期間
                Statistics=[metric['Stat']]                        # 取得する統計情報の種類
            )

            results.append(response)

    # 結果をCSVに保存するなどの処理
    return results
