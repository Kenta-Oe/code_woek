# EC2およびRDS統合用のCloudFormationテンプレート

このCloudFormationテンプレートは、EC2インスタンスとRDSインスタンスを作成し、データベースの初期化を行うものです。

## テンプレートの説明

このテンプレートは、指定されたVPCとサブネット内にEC2インスタンスとRDSインスタンスをセットアップします。EC2インスタンスにはMySQLクライアントがインストールされ、RDSインスタンスに接続してデータベースを初期化します。初期化にはサンプルテーブルとデータが含まれます。

## パラメータ

- **VPC**: リソースのためのVPC ID。
- **SubnetId**: EC2インスタンスのためのサブネットID。
- **KeyName**: EC2インスタンスへのSSHアクセスを許可するキー・ペア。
- **SecurityGroupId**: 既存のセキュリティグループのID。
- **InstanceType**: EC2インスタンスタイプ。デフォルトは`t2.micro`。
- **VolumeSize**: EBSボリュームのサイズ（GiB）。デフォルトは10 GiB。
- **VolumeType**: EBSボリュームのタイプ。デフォルトは`gp2`。
- **DBInstanceIdentifier**: データベースインスタンスの識別子。
- **AllocatedStorage**: データベースのサイズ（GB）。デフォルトは20 GB。
- **DBInstanceClass**: データベースインスタンスのコンピュートおよびメモリ容量。デフォルトは`db.t3.micro`。
- **Engine**: 使用するデータベースエンジン。デフォルトは`mysql`。
- **MasterUsername**: データベースのマスターユーザー名。
- **MasterUserPassword**: データベースのマスターパスワード。
- **DBName**: データベースの名前。
- **BackupRetentionPeriod**: バックアップを保持する日数。デフォルトは7日。
- **MultiAZ**: データベースインスタンスがマルチAZデプロイメントかどうかを指定。デフォルトは`false`。
- **StorageType**: データベースインスタンスに関連付けられるストレージタイプ。デフォルトは`gp2`。
- **EngineVersion**: データベースエンジンのバージョン。
- **AutoMinorVersionUpgrade**: マイナーエンジンアップグレードが自動的に適用されるかどうかを示す。デフォルトは`true`。
- **PubliclyAccessible**: データベースインスタンスがパブリックにアクセス可能かどうかを示す。デフォルトは`false`。
- **SubnetA**: RDSインスタンスのためのサブネットID。
- **SubnetB**: RDSインスタンスのためのもう1つのサブネットID。

## リソース

### EC2インスタンス

- **InstanceType**: `InstanceType`パラメータを参照。
- **KeyName**: `KeyName`パラメータを参照。
- **ImageId**: インスタンスタイプとリージョンに基づいて適切なAMI IDを決定するマッピングを参照。
- **SubnetId**: `SubnetId`パラメータを参照。
- **SecurityGroupIds**: `SecurityGroupId`パラメータを参照。
- **BlockDeviceMappings**: `VolumeSize`および`VolumeType`パラメータに基づいてEBSボリュームのサイズとタイプを設定。
- **UserData**: MySQLクライアントをインストールし、データベースを初期化するユーザーデータスクリプト。

### RDSインスタンス

- **DBInstanceIdentifier**: `DBInstanceIdentifier`パラメータを参照。
- **AllocatedStorage**: `AllocatedStorage`パラメータを参照。
- **DBInstanceClass**: `DBInstanceClass`パラメータを参照。
- **Engine**: `Engine`パラメータを参照。
- **MasterUsername**: `MasterUsername`パラメータを参照。
- **MasterUserPassword**: `MasterUserPassword`パラメータを参照。
- **DBName**: `DBName`パラメータを参照。
- **VPCSecurityGroups**: `MyDBSecurityGroup`リソースを参照。
- **BackupRetentionPeriod**: `BackupRetentionPeriod`パラメータを参照。
- **DBParameterGroupName**: `MyDBParameterGroup`リソースを参照。
- **MultiAZ**: `MultiAZ`パラメータを参照。
- **StorageType**: `StorageType`パラメータを参照。
- **EngineVersion**: `EngineVersion`パラメータを参照。
- **AutoMinorVersionUpgrade**: `AutoMinorVersionUpgrade`パラメータを参照。
- **PubliclyAccessible**: `PubliclyAccessible`パラメータを参照。
- **Tags**: RDSインスタンスにタグを追加。
- **DBSubnetGroupName**: `MyDBSubnetGroup`リソースを参照。

### DBパラメータグループ

- **Description**: DBインスタンスのパラメータグループ。
- **Family**: パラメータグループファミリーを指定。
- **Parameters**: DBインスタンスのカスタムパラメータ。

### DBセキュリティグループ

- **GroupDescription**: セキュリティグループの説明。
- **VpcId**: `VPC`パラメータを参照。
- **SecurityGroupIngress**: ポート3306でRDSインスタンスへのインバウンドアクセスを許可。

### DBサブネットグループ

- **DBSubnetGroupDescription**: サブネットグループの説明。
- **SubnetIds**: `SubnetA`および`SubnetB`パラメータを参照。

## マッピング

### AWSInstanceType2Arch

各インスタンスタイプのアーキテクチャを定義。

### AWSRegionArch2AMI

各リージョンとアーキテクチャのためのAMI IDを定義。

## 使用方法

このCloudFormationテンプレートを使用するには、必要なパラメータを提供し、AWS環境にデプロイします。これにより、データベースが初期化された状態でEC2インスタンスとRDSインスタンスが作成されます。
