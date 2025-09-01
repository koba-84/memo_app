import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"
    JWT_SECRET_KEY = (
        os.environ.get("JWT_SECRET_KEY") or "super-secret-jwt-key"
    )  # 🔥 追加！
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    # ローカライズ設定
    BABEL_DEFAULT_LOCALE = "ja"
    BABEL_DEFAULT_TIMEZONE = "Asia/Tokyo"
    LANGUAGES = ["en", "ja"]
    BABEL_TRANSLATION_DIRECTORIES = "translations"
    BABEL_DOMAIN = "messages"
