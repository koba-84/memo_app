# 📝 Flaskメモ帳アプリ

Python (Flask) 製のシンプルなメモ帳アプリです。ユーザー登録・ログイン後にメモを作成・編集・削除できます。

## 🚀 機能概要

- ユーザー登録・ログイン
- メモの作成・閲覧・編集・削除（ユーザーごと）
- SQLiteによる簡易DB管理
- Jinja2テンプレートでHTML生成

---

## 🧱 ディレクトリ構成
memo_app/
├── app.py
├── config.py
├── forms.py
├── models.py
├── routes.py
├── init_db.py
├── requirements.txt
├── static/
│ └── style.css
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── register.html
│ ├── index.html
│ └── edit.html
└── README.md
