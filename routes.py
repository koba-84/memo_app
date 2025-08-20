from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Memo, Tag, memo_tags
from forms import LoginForm, MemoForm, RegisterForm
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db, login_manager  # extensions.py からインポート
from flask_jwt_extended import create_access_token, jwt_required

routes = Blueprint("routes", __name__)


def get_or_create_tags(tag_string):
    tag_list = [t.strip() for t in tag_string.split(",") if t.strip()]
    tags = []
    for name in tag_list:
        tag = Tag.query.filter_by(name=name).first()
        if not tag:
            tag = Tag(name=name)
            db.session.add(tag)
        tags.append(tag)
    return tags


@routes.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


"""
@routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("routes.index"))
        flash("ユーザー名またはパスワードが間違っています")
    return render_template("login.html", form=form)
"""


@routes.route("/logout")
@jwt_required()
def logout():
    logout_user()
    return redirect(url_for("routes.login"))


@routes.route("/")
def index():
    return render_template("index.html")


@routes.route("/edit/<int:memo_id>", methods=["GET", "POST"])
@jwt_required()
def edit(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    if memo.author != current_user:
        flash("編集する権限がありません")
        return redirect(url_for("routes.index"))

    form = MemoForm(obj=memo)
    if form.validate_on_submit():
        memo.title = form.title.data
        memo.content = form.content.data
        db.session.commit()
        return redirect(url_for("routes.index"))

    return render_template("edit.html", form=form)


@routes.route("/delete/<int:memo_id>", methods=["POST"])
@jwt_required()
def delete(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    if memo.author != current_user:
        flash("削除する権限がありません")
        return redirect(url_for("routes.index"))

    db.session.delete(memo)
    db.session.commit()
    return redirect(url_for("routes.index"))


@routes.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")
