# migrations/env.py
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# 追加: Flaskアプリ/SQLAlchemyをロードする
from app import create_app
from extensions import db  # db = SQLAlchemy()

# Alembic Config オブジェクト
config = context.config

# ログ設定
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Flaskアプリ作成 & アプリコンテキスト
app = create_app()
app.app_context().push()

# Alembic が参照すべきメタデータ（モデルの集合）
target_metadata = db.metadata


# DB URL をアプリ設定から取得
def get_url():
    # 優先: 環境変数 DATABASE_URL、なければ Flask の設定
    return os.getenv("DATABASE_URL") or app.config.get("SQLALCHEMY_DATABASE_URI")


def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # SQLiteでも安全に列変更できるように
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,  # SQLite対応
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
