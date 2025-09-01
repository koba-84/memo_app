from flask import Flask, jsonify, request, session
from utils import to_jst
from api import api
from flask_jwt_extended import JWTManager
from flask_babel import (
    Babel,
    gettext as _,
    ngettext as n_,
    format_datetime,
    format_date,
    format_time,
    LazyString,
    lazy_gettext,
)
from extensions import db, login_manager
import logging
from werkzeug.serving import WSGIRequestHandler

# ---- logging (任意) ----
logging.basicConfig(level=logging.DEBUG)
WSGIRequestHandler.log_request = lambda self, code="-", size="-": logging.info(
    "%s %s %s %s", self.command, self.path, code, size
)

# ---- 拡張はモジュールスコープで生成し、init_appで結びつける ----
babel = Babel()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # ---- JWT コールバック ----
    jwt.init_app(app)

    @jwt.unauthorized_loader
    def custom_unauthorized_response(err_str):
        app.logger.warning(f"[JWT ERROR] unauthorized_loader: {err_str}")
        return jsonify({"msg": "Missing or invalid JWT", "error": err_str}), 401

    @jwt.invalid_token_loader
    def custom_invalid_token_callback(err_str):
        app.logger.warning(f"[JWT ERROR] invalid_token_loader: {err_str}")
        return jsonify({"msg": "Invalid JWT", "error": err_str}), 422

    @jwt.expired_token_loader
    def custom_expired_token_callback(jwt_header, jwt_payload):
        app.logger.info(f"[JWT ERROR] expired_token_loader: {jwt_payload}")
        return jsonify({"msg": "Token has expired"}), 401

    # ---- Jinja2 に util を注入 ----
    @app.context_processor
    def inject_timezone_utils():
        return dict(to_jst=to_jst)

    # ---- Babel 4.x の selector 関数（新API）----
    def select_locale():
        # ① URLクエリ優先 (?lang=ja/en)
        lang = request.cookies.get("lang")
        if lang in app.config["LANGUAGES"]:
            return lang

        # ② セッション（ユーザーが以前選んだやつ）
        lang = session.get("lang")
        if lang in app.config["LANGUAGES"]:
            return lang

        # ③ ブラウザの Accept-Language
        return request.accept_languages.best_match(app.config["LANGUAGES"]) or "ja"

    def select_timezone():
        # 必要なら。未使用なら "Asia/Tokyo" 固定でもOK
        return "Asia/Tokyo"

    babel.init_app(
        app,
        default_locale="ja",
        default_timezone="Asia/Tokyo",
        locale_selector=select_locale,
        timezone_selector=select_timezone,
    )

    # ---- DB / LoginManager ----
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "routes.login"  # 例: Blueprint名.routesのlogin

    @app.context_processor
    def inject_i18n_helpers():
        # get_locale() は Locale オブジェクトなので文字列化して返す
        return dict(
            get_locale=lambda: str(select_locale()),
            get_timezone=select_timezone,
        )

    @login_manager.user_loader
    def load_user(user_id: str):
        from models import User

        try:
            # SQLAlchemy 2.x なら db.session.get が推奨
            return db.session.get(User, int(user_id))
        except Exception:
            return None

    # ---- Blueprint 登録はアプリコンテキスト内で ----
    with app.app_context():
        from models import User, Memo, Tag, memo_tags  # noqa: F401

        from routes import routes

        app.register_blueprint(routes)

        app.register_blueprint(api, url_prefix="/api")

    return app


# WSGIエントリポイント（Alembicのenv.pyからもimportされる想定）
app = create_app()
