# ベースイメージ
FROM python:3.10-slim

# 作業ディレクトリを作成
WORKDIR /app

# 依存ファイルをコピー
COPY requirements.txt .

# ライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリコードをコピー
COPY . .

# ポート開放
EXPOSE 5000

# 実行コマンド
CMD ["python", "app.py"]
