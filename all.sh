#!/bin/zsh

# 1. Docker Desktop起動（非同期）
open -a Docker

# 2. Dockerが起動するまで待つ
while ! docker system info > /dev/null 2>&1; do
    echo "Waiting for Docker Desktop to start..."
    sleep 2
done

# 3. アプリのディレクトリへ移動
cd "/Users/ryoma/Desktop/study/leetcode/memo_app"

# 4. Dockerコンテナ起動（バックグラウンド）
docker compose up -d

# 5. アプリが応答するまで待機
while ! curl -s http://127.0.0.1:5050 > /dev/null; do
    echo "Waiting for app to be ready..."
    sleep 1
done

# 6. ブラウザで開く
open "http://127.0.0.1:5050"
