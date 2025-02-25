# GitPy App

## 概要

GitPy Appは、Flaskベースのウェブアプリケーションで、ローカル環境でのGitリポジトリ管理を簡単に行えるツールです。リポジトリの作成、ファイル管理、ブランチ操作などの基本的なGit機能を提供します。

## 主な機能

- リポジトリの作成
- ファイルのアップロード、編集、作成
- ブランチ管理（作成、チェックアウト）
- ファイルの履歴表示
- シンタックスハイライト
- 簡易的なユーザー認証システム

## 必要な環境

- Python 3.x
- Flask
- GitPython
- その他の依存ライブラリは`requirements.txt`を参照

## インストール手順

1. リポジトリをクローン
```bash
git clone [リポジトリURL]
cd gitpy_app
```

2. 仮想環境の作成（推奨）
```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

3. 依存ライブラリのインストール
```bash
pip install -r requirements.txt
```

## 起動方法

```bash
python run.py
```

デフォルトでは`http://127.0.0.1:5000/`で起動します。

## 設定

- `config.py`: アプリケーションの基本設定
- デバッグモード、リポジトリの保存先、アップロードファイルサイズ制限などを調整可能

## ユーザー認証

現在は簡易的な認証システムが実装されています。
- ユーザー名: `user1`
- パスワード: `password123`

## 主要なディレクトリ構造

```
gitpy_app/
│
├── app.py          # メインアプリケーション
├── config.py       # 設定ファイル
├── run.py          # アプリケーション起動スクリプト
├── repositories/   # Gitリポジトリの保存先
├── static/         # 静的ファイル（CSS、JavaScript）
└── templates/      # HTMLテンプレート
```

## 注意点

- これは開発用のアプリケーションです。
- セキュリティ面での本番環境での使用は推奨されません。
- ユーザー認証は非常にシンプルな実装となっています。

## ライセンス

[適切なライセンスを追加]

## 作者

[作者名]
