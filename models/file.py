from exts import db
from datetime import datetime

class ApkInfoModel(db.Model):
    __tablename__ = "apk_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(100), nullable=False, )
    version =db.Column(db.String(10), nullable=False, )
    join_time = db.Column(db.DateTime, default=datetime.now)
