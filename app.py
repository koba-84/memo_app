from flask import Flask
from utils import to_jst
from api import api
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
from flask import Blueprint, jsonify, request
from extensions import db, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    # jwt = JWTManager(app)
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def custom_unauthorized_response(err_str):
        print(f"[JWT ERROR] unauthorized_loader: {err_str}")
        return jsonify({"msg": "Missing or invalid JWT", "error": err_str}), 401

    @jwt.invalid_token_loader
    def custom_invalid_token_callback(err_str):
        print(f"[JWT ERROR] invalid_token_loader: {err_str}")
        return jsonify({"msg": "Invalid JWT", "error": err_str}), 422

    @jwt.expired_token_loader
    def custom_expired_token_callback(jwt_header, jwt_payload):
        print(f"[JWT ERROR] expired_token_loader: {jwt_payload}")
        return jsonify({"msg": "Token has expired"}), 401

    @app.context_processor
    def inject_timezone_utils():
        return dict(to_jst=to_jst)

    # 拡張を初期化
    db.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "routes.login"

    # 遅延インポート
    with app.app_context():
        from models import User, Memo, Tag, memo_tags  # ここでモデルをインポート

        db.create_all()  # ここで初期化

        # user_loader を init_app の後に定義
        @login_manager.user_loader
        def load_user(user_id):
            from models import User  # ここでUserモデルをインポート

            return User.query.get(int(user_id))

        # routes.py の Blueprint を登録
        from routes import routes

        app.register_blueprint(routes)
        # api.py の Blueprint を登録
        app.register_blueprint(api, url_prefix="/api")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
