# CloudFormation テンプレート：シングル EC2 インスタンスでの LAMP スタック

## 説明
この AWS CloudFormation テンプレートは、シングル EC2 インスタンスを使用して LAMP スタック（Apache、PHP、MySQL）を作成する。テンプレートには以下の機能が含まれる：
- Apache のインストール
- PHP のインストール
- MySQL のインストールと設定
- インスタンス起動時のパッケージおよびファイルのデプロイ

## パラメータ
テンプレートには以下のパラメータが含まれている：

- `KeyName`
  - **説明**: インスタンスへの SSH アクセスを有効にする既存の EC2 キーペアの名前
  - **タイプ**: `AWS::EC2::KeyPair::KeyName`
  - **制約説明**: 既存の EC2 キーペアの名前である必要がある

- `DBName`
  - **デフォルト**: `MyDatabase`
  - **説明**: MySQL データベース名
  - **タイプ**: `String`
  - **最小長**: 1
  - **最大長**: 64
  - **許可されるパターン**: `[a-zA-Z][a-zA-Z0-9]*`
  - **制約説明**: 文字で始まり、英数字のみを含む必要がある

- `DBUser`
  - **NoEcho**: `true`
  - **説明**: MySQL データベースアクセス用のユーザー名
  - **タイプ**: `String`
  - **最小長**: 1
  - **最大長**: 16
  - **許可されるパターン**: `[a-zA-Z][a-zA-Z0-9]*`
  - **制約説明**: 文字で始まり、英数字のみを含む必要がある

- `DBPassword`
  - **NoEcho**: `true`
  - **説明**: MySQL データベースアクセス用のパスワード
  - **タイプ**: `String`
  - **最小長**: 1
  - **最大長**: 41
  - **許可されるパターン**: `[a-zA-Z0-9]*`
  - **制約説明**: 英数字のみを含む必要がある

- `DBRootPassword`
  - **NoEcho**: `true`
  - **説明**: MySQL のルートパスワード
  - **タイプ**: `String`
  - **最小長**: 1
  - **最大長**: 41
  - **許可されるパターン**: `[a-zA-Z0-9]*`
  - **制約説明**: 英数字のみを含む必要がある

- `InstanceType`
  - **説明**: Web サーバー EC2 インスタンスタイプ
  - **タイプ**: `String`
  - **デフォルト**: `t2.small`
  - **許可される値**: 多数の EC2 インスタンスタイプ
  - **制約説明**: 有効な EC2 インスタンスタイプである必要がある

- `SSHLocation`
  - **説明**: EC2 インスタンスへの SSH アクセスに使用できる IP アドレス範囲
  - **タイプ**: `String`
  - **最小長**: 9
  - **最大長**: 18
  - **デフォルト**: `0.0.0.0/0`
  - **許可されるパターン**: `(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})`
  - **制約説明**: x.x.x.x/x の形式の有効な IP CIDR 範囲である必要がある

## リソース
以下のリソースが作成される：

- `WebServerInstance`
  - **タイプ**: `AWS::EC2::Instance`
  - **プロパティ**:
    - `InstanceType`: パラメータ `InstanceType` から取得
    - `KeyName`: パラメータ `KeyName` から取得
    - `ImageId`: 適切な AMI を `AWSRegionArch2AMI` マッピングから取得
    - `SecurityGroups`: セキュリティグループ `WebServerSecurityGroup` を参照
    - `UserData`: インスタンス起動時に実行されるスクリプトを含む
  - **メタデータ**:
    - `AWS::CloudFormation::Init`:
      - **configSets**: `Install` および `Configure` の設定
      - **packages**: `yum` パッケージのインストール
      - **files**: ファイル `/var/www/html/index.php` などの作成と設定
      - **services**: `mysqld`, `httpd`, および `cfn-hup` の設定

- `WebServerSecurityGroup`
  - **タイプ**: `AWS::EC2::SecurityGroup`
  - **プロパティ**:
    - **GroupDescription**: "Enable HTTP access via port 80"
    - **SecurityGroupIngress**: ポート 80 と 22 へのアクセスを許可

## 出力
- `WebsiteURL`
  - **説明**: 新しく作成された LAMP スタックの URL
  - **値**: EC2 インスタンスの `PublicDnsName` から生成された URL
