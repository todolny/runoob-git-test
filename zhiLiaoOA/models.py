from exts import db
from datetime import datetime
#用户数据
class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False,unique=True)
    join_time=db.Column(db.DateTime,default=datetime.now)

#邮箱和验证码
class EmailCaptchaModedl(db.Model):
    __tablename__='email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha=db.Column(db.String(100),nullable=False)

#问题
class QuestionModel(db.Model):
    __tablename__="question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String(100), nullable=False)
    content=db.Column(db.Text, nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now())
    #外键关联
    author_id=db.Column(db.Integer, db.ForeignKey("user.id"))
    author=db.relationship(UserModel, backref="questions")

#回答
class AnswerModel(db.Model):
    __tablename__="answer"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    content=db.Column(db.Text, nullable=False)
    create_time=db.Column(db.DateTime, default=datetime.now())

    #外键
    question_id=db.Column(db.Integer, db.ForeignKey("question.id"))
    author_id=db.Column(db.Integer, db.ForeignKey("user.id"))

    #关系
    question=db.relationship(QuestionModel, backref=db.backref("answers",order_by=create_time.desc()))
    author=db.relationship(UserModel,backref="answers")#应该是QuestionModel能够通过.answers访问其对应的所有answer，而