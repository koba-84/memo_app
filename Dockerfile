# ==== Base ===============================================================
FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# OS依存の最低限（psycopg2 を将来使うなら libpq-dev を追加）
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    gcc \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 依存インストール（層を活かすために先に requirements のみコピー）
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt 
# アプリコード
COPY . .

# SQLite の永続化先（Compose で ./instance をマウントする想定）
RUN mkdir -p /app/instance

# 実行用エントリポイント
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 非root 実行（任意）
RUN useradd -ms /bin/bash appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000
ENTRYPOINT ["/entrypoint.sh"]
