# CloudFormation テンプレート：Apache インストールとユーザー作成を伴う EC2 インスタンス

## 説明
この AWS CloudFormation テンプレートは、AKMS、EBS、プライベート IP、および既存のセキュリティグループを使用する EC2 インスタンスを作成する。

## パラメータ
テンプレートには以下のパラメータが含まれている：

### `InstanceType`
- **説明**: Webサーバー EC2 インスタンスタイプ
- **タイプ**: `String`
- **デフォルト**: `t2.small`
- **制約説明**: 有効な EC2 インスタンスタイプである必要がある

### `ImageId`
- **説明**: Webサーバー EC2 AMI ID
- **タイプ**: `String`
- **デフォルト**: `ami-064d2a8f528240c59`

### `SecurityGroupId`
- **説明**: 既存のセキュリティグループの ID
- **タイプ**: `AWS::EC2::SecurityGroup::Id`
- **許可されるパターン**: `sg-[a-zA-Z0-9]+`
- **制約説明**: 有効なセキュリティグループ ID である必要がある

### `SubnetId`
- **説明**: インスタンスがデプロイされるサブネット ID
- **タイプ**: `AWS::EC2::Subnet::Id`

### `PrivateIpAddress`
- **説明**: EC2 インスタンスへの SSH アクセスに使用される IP アドレス範囲
- **タイプ**: `String`
- **最小長**: 9
- **最大長**: 18
- **デフォルト**: `0.0.0.0/0`
- **許可されるパターン**: `(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})`

### `KeyName`
- **説明**: インスタンスへの SSH アクセスを有効にする既存の EC2 キーペアの名前
- **タイプ**: `AWS::EC2::KeyPair::KeyName`
- **制約説明**: 既存の EC2 キーペアの名前である必要がある

### `EbsVolumeSize`
- **説明**: EBS ボリュームのサイズ (GB)
- **タイプ**: `Number`
- **デフォルト**: 20
- **最小値**: 1
- **最大値**: 16384

## リソース
以下のリソースが作成される：

### `MyEC2Instance`
- **タイプ**: `AWS::EC2::Instance`
- **プロパティ**:
  - **InstanceType**: `InstanceType` パラメータから取得
  - **KeyName**: `KeyName` パラメータから取得
  - **ImageId**: `ImageId` パラメータから取得
  - **SubnetId**: `SubnetId` パラメータから取得
  - **PrivateIpAddress**: `PrivateIpAddress` パラメータから取得
  - **SecurityGroupIds**: `SecurityGroupId` パラメータから取得
  - **BlockDeviceMappings**:
    - **DeviceName**: `/dev/xvda`
    - **Ebs**:
      - **VolumeSize**: `EbsVolumeSize` パラメータから取得
      - **VolumeType**: `gp2`
      - **Encrypted**: `true`

このテンプレートは、指定されたパラメータに基づいて EC2 インスタンスを作成し、EBS ボリュームをマウントし、セキュリティグループを適用する。
