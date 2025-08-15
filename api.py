from flask import Blueprint, jsonify, request, abort
from models import db, Memo, User, Tag
from datetime import datetime
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    JWTManager,
)

from datetime import timedelta

api = Blueprint("api", __name__, url_prefix="/api")
jwt = JWTManager()


@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"msg": "username と password を指定してください"}), 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"msg": "ユーザー名またはパスワードが正しくありません"}), 401

    access_token = create_access_token(
        identity=str(user.id), expires_delta=timedelta(hours=1)
    )

    return jsonify(access_token=access_token, user_id=user.id), 200


# メモ一覧
@api.route("/memos", methods=["GET"])
@jwt_required()
def get_memos():
    print("[DEBUG] headers:", request.headers)
    try:
        # user_id = 1
        user_id = int(get_jwt_identity())
        print(f"[DEBUG] User ID: {user_id}")  # ← ここが出るかログを見て
        if not user_id:
            return jsonify({"msg": "Invalid token - user_id is None"}), 400
    except Exception as e:
        print(f"[ERROR] JWT decoding failed: {e}")
        return jsonify({"msg": "JWT decoding failed", "error": str(e)}), 400

    # user_id = get_jwt_identity()
    # print(f"User ID: {user_id}")  # デバッグ用ログ
    q = request.args.get("q", "").strip()

    if q:
        memos = (
            Memo.query.filter(
                Memo.user_id == user_id,
                db.or_(
                    Memo.title.ilike(f"%{q}%"),
                    Memo.content.ilike(f"%{q}%"),
                    Memo.tags.any(Tag.name.ilike(f"%{q}%")),
                ),
            )
            .order_by(Memo.created_at.desc())
            .all()
        )
    else:
        memos = (
            Memo.query.filter_by(user_id=user_id).order_by(Memo.created_at.desc()).all()
        )

    return jsonify(
        [
            {
                "id": m.id,
                "title": m.title,
                "content": m.content,
                "created_at": m.created_at.isoformat(),
                "tags": [t.name for t in m.tags],
            }
            for m in memos
        ]
    )


# メモ作成
@api.route("/memos", methods=["POST"])
@jwt_required()
def create_memo():
    user_id = int(get_jwt_identity())
    if not user_id:
        abort(401, "認証が必要です")

    data = request.json
    if not data or "title" not in data or "content" not in data:
        abort(400, "title, content は必須です")

    user = User.query.get(user_id)
    if not user:
        abort(404, f"user_id={user_id} のユーザーが存在しません")

    # メモ作成
    memo = Memo(
        title=data["title"],
        content=data["content"],
        user=user,
        created_at=datetime.now(),
    )

    # タグ処理
    if "tags" in data:
        for tag_name in data["tags"]:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            memo.tags.append(tag)

    db.session.add(memo)
    db.session.commit()

    return jsonify(memo.to_dict()), 201


# メモ更新
@api.route("/memos/<int:memo_id>", methods=["PUT"])
@jwt_required()
def update_memo(memo_id):
    user_id = int(get_jwt_identity())
    if not user_id:
        abort(401, "認証が必要です")
    memo = Memo.query.get_or_404(memo_id)
    data = request.json
    if "title" in data:
        memo.title = data["title"]
    if "content" in data:
        memo.content = data["content"]
    db.session.commit()
    return jsonify(memo.to_dict())


# メモ削除
@api.route("/memos/<int:memo_id>", methods=["DELETE"])
@jwt_required()
def delete_memo(memo_id):
    user_id = int(get_jwt_identity())
    if not user_id:
        abort(401, "認証が必要です")
    memo = Memo.query.get_or_404(memo_id)
    db.session.delete(memo)
    db.session.commit()
    return jsonify({"message": "deleted"}), 204


@api.route("/test-token", methods=["GET"])
@jwt_required()
def test_token():
    return jsonify(msg="トークンは有効です", user_id=get_jwt_identity()), 200
