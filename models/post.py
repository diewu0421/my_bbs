from datetime import datetime

from exts import db


class BoardModel(db.Model):
    __tablename__ = "board"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)


class PostModel(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    read_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    board_id = db.Column(db.Integer, db.ForeignKey("board.id"))
    board = db.relationship("BoardModel", backref="posts")

    author_id = db.Column(db.String(100), db.ForeignKey("user.id"))
    author = db.relationship("UserModel", backref="posts")




class CommentModel(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    author_id = db.Column(db.String(100), db.ForeignKey("user.id"))
    # post = db.relationship("PostModel", backref="comments")
    # author = db.relationship("UserModel", backref="comments")
    # 一个评论属于一条帖子，属于一个作者
    post = db.relationship("PostModel", backref=db.backref('comments', order_by=create_time.desc(), lazy="dynamic"))
    author = db.relationship("UserModel", backref='comments')