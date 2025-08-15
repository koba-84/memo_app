from flask_login import UserMixin
from datetime import datetime
from extensions import db  # extensions.py からインポート


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    memos = db.relationship("Memo", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"


memo_tags = db.Table(
    "memo_tags",
    db.Column("memo_id", db.Integer, db.ForeignKey("memos.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    memos = db.relationship("Memo", secondary=memo_tags, back_populates="tags")

    def __repr__(self):
        return f"<Tag {self.name}>"


class Memo(db.Model):
    __tablename__ = "memos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="memos")
    tags = db.relationship("Tag", secondary=memo_tags, back_populates="memos")

    def __repr__(self):
        return f"<Memo {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "user": {"id": self.user.id, "username": self.user.username},
            "tags": [tag.name for tag in self.tags],
        }
