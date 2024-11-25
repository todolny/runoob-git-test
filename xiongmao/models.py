from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    #SQLAlchemy 的 db.Column 类型严格区分大小写。如果写错了 db.Datetime，它会尝试在 SQLAlchemy 的扩展中寻找 Datetime 属性。但这个属性不存在，于是抛出了 AttributeError。

