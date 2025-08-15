from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("ユーザー名", validators=[DataRequired(), Length(max=64)])
    password = PasswordField("パスワード", validators=[DataRequired()])
    submit = SubmitField("ログイン")


class MemoForm(FlaskForm):
    title = StringField("タイトル", validators=[DataRequired(), Length(max=100)])
    content = TextAreaField("内容")
    tags = StringField("タグ（カンマ区切り）")  # ★ 追加
    submit = SubmitField("保存")


class RegisterForm(FlaskForm):
    username = StringField("ユーザー名", validators=[DataRequired(), Length(max=64)])
    password = PasswordField("パスワード", validators=[DataRequired()])
    submit = SubmitField("登録")
