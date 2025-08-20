# メモアプリケーション

これは Flask を使用して構築された、シンプルなメモ管理アプリケーションです。ユーザーはアカウントを作成し、メモを作成、編集、削除することができます。

## 主な機能

- ユーザー登録・ログイン機能 (JWTベースの認証)
- メモのCRUD (作成、閲覧、更新、削除)
- タグ付け機能

## 技術スタック

### バックエンド
- **フレームワーク**: Flask
- **ORM**: SQLAlchemy
- **データベースマイグレーション**: Alembic
- **認証**: Flask-Login, Flask-JWT-Extended
- **Webサーバー**: Gunicorn

### フロントエンド
- **CSSフレームワーク**: Bootstrap 5

### データベース
- **開発/本番**: PostgreSQL
- **ローカルテスト (過去)**: SQLite

### コンテナ
- Docker, Docker Compose

## ディレクトリ構成

```
.
├─── alembic.ini              # Alembicの設定ファイル
├─── app.py                   # Flaskアプリケーションのメインファイル
├─── config.py                # 設定ファイル
├─── docker-compose.yaml      # Docker Composeの設定ファイル
├─── Dockerfile               # Dockerイメージのビルド設定
├─── extensions.py            # Flask拡張機能のインスタンス化
├─── forms.py                 # WTFormsを使用したフォーム定義
├─── models.py                # SQLAlchemyのモデル定義
├─── requirements.txt         # Pythonの依存パッケージリスト
├─── routes.py                # ルーティング定義
├─── templates/               # HTMLテンプレート
│    ├─── base.html
│    ├─── edit.html
│    ├─── index.html
│    ├─── login.html
│    └─── register.html
├─── migrations/              # Alembicのマイグレーションスクリプト
└─── pgdata/                  # (ローカル) PostgreSQLのデータボリューム
```

## セットアップと実行方法

### Dockerを使用する場合 (推奨)

1.  リポジトリをクローンします。
    ```bash
    git clone <repository_url>
    cd memo_app
    ```

2.  `.env` ファイルを作成し、環境変数を設定します。(必要に応じて)

3.  Docker Compose を使用してコンテナをビルドし、起動します。
    ```bash
    docker-compose up --build
    ```
    これにより、WebアプリケーションとPostgreSQLデータベースが起動します。
    初回起動時に `alembic upgrade head` が実行され、データベースのテーブルが自動的に作成されます。

4.  ブラウザで `http://localhost:5050` にアクセスします。

### ローカルで直接実行する場合

1.  リポジトリをクローンします。
    ```bash
    git clone <repository_url>
    cd memo_app
    ```

2.  Pythonの仮想環境を作成し、有効化します。
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  必要なPythonパッケージをインストールします。
    ```bash
    pip install -r requirements.txt
    ```

4.  PostgreSQLデータベースを準備し、`.env` ファイルに `DATABASE_URL` を設定します。
    例: `DATABASE_URL=postgresql://user:password@localhost:5432/dbname`

5.  Alembicを使用してデータベースをマイグレーションします。
    ```bash
    alembic upgrade head
    ```

6.  Flaskアプリケーションを起動します。
    ```bash
    flask run
    ```

7.  ブラウザで `http://localhost:5000` にアクセスします。

## APIエンドポイント

このアプリケーションは、Web UIに加えてRESTful APIも提供します。

-   `/api/register` (POST): ユーザー登録
-   `/api/login` (POST): ログイン (JWTトークン発行)
-   `/api/memos` (GET, POST): メモの一覧取得、新規作成
-   `/api/memos/<id>` (GET, PUT, DELETE): 特定のメモの取得、更新、削除

APIを使用する際は、ログイン後に取得したJWTトークンを `Authorization` ヘッダーに `Bearer <token>` の形式で含める必要があります。