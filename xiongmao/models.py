from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"#注意数据库表名不要出现有大写的情况，因为表名显示都为小写，这里用大写会导致后续更新数据库数据时卡住无法进行下一步
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    # SQLAlchemy 的 db.Column 类型严格区分大小写。如果写错了 db.Datetime，它会尝试在 SQLAlchemy 的扩展中寻找 Datetime 属性。但这个属性不存在，于是抛出了 AttributeError。


class EmailModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)


class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    #外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(UserModel, backref="questions")


class AnswerModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    #外键
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    #关系
    question = db.relationship(QuestionModel, backref=db.backref("answers", order_by=create_time.desc()))
    author = db.relationship(UserModel, backref="answers")
