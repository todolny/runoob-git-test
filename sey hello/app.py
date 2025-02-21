import sys
import click
import pymysql
import wtforms as wtforms
from flask_moment import Moment
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

from wtforms.validators import Length, EqualTo, DataRequired, ValidationError

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)

moment = Moment(app)#加入Moment参数

HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "123456"
DATABASE = "xiongmaomovies"
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# SQLALCHEMY_DATABASE_URI = DB_URI
# 加载配置
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 在扩展类实例化前加载配置,使用蓝图的话db = SQLAlchemy(app)中的app要去掉,因为要先配置
db = SQLAlchemy()
db.init_app(app)  # 然后再在这里使db和app绑定，绑定数据库
# db.init_app(app)#在这里使db和app绑定，绑定数据库   原本应该是有这个和app绑定的操作，但是看上面添加了app不知道是否可以代替
migrate = Migrate(app, db)


app.config['SECRET_KEY'] = 'your_unique_and_secret_key_here'#想要使用flash弹出信息还必须添加相应的密匙,这个原因是什么


class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    message = db.Column(db.String(200), nullable=False)  # 留言
    cipher = db.Column(db.String(20))  # anhao
    time = db.Column(db.DateTime, default=datetime.now)  # 发布时间


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    # user = User.query.first()
    return render_template('404.html'), 404  # 返回模板和状态码


@app.cli.command()
def forge():
    """Generate fake data."""
    with app.app_context():
        db.create_all()  # 创建所有表

        # 添加全局变量的数据
        questions = [
            {'name': 'boom', 'message': '爆竹炸响岁岁平安', 'cipher': '我的世界', 'time': datetime.now()},  # 使用当前时间
            {'name': '星雨', 'message': '晴天之雨如夏日流星般璀璨坠落', 'cipher': '我的世界', 'time': datetime.now()},
        ]

        # 添加问题到数据库
        for q in questions:
            question = Question(name=q['name'], message=q['message'], cipher=q['cipher'], time=q['time'])
            db.session.add(question)  # 在循环内部添加到会话中

        db.session.commit()  # 提交会话
        click.echo('Done.')  # 输出完成信息


# 可以拿表单做验证
class QuestionForm(wtforms.Form):
    name = wtforms.StringField(validators=[Length(min=1, max=100, message="名称格式错误")])
    message = wtforms.StringField(validators=[Length(min=1, message="内容格式错误")])
    cipher = wtforms.StringField(validators=[Length(min=1)])
    time = wtforms.DateTimeField(validators=[DataRequired()])  # 使用 DateTimeField

def validate_cipher(form, field):
    if field != "大熊猫乐园":
        raise ValidationError("暗号有误，你是谁！")


@app.route('/', methods=['GET', 'POST'])
def index():  # put application's code here
    # 获取当前页码，默认为 1
    # page = request.args.get("page", 1, type=int)
    # # 分页，每页 10 条记录
    # questions = Question.query.order_by(Question.time.desc()).paginate(page=page, per_page=10)#拿数据库的数据

    if request.method == 'POST':
        form = QuestionForm(request.form)
        if form.validate():
            name = form.name.data
            message = form.message.data
            cipher = form.cipher.data
            if cipher != "大熊猫乐园":
                raise ValidationError("暗号有误，你是谁！")#这里的错误显示得看情况怎么修改为弹窗类提示
            else:
                # datetime = form.datetime.data
                question = Question(name=name, message=message, cipher=cipher)
                db.session.add(question)
                db.session.commit()
                flash('Your message have been sent to the world!')
                return redirect(url_for("index"))
        else:
            print(form.errors)
            return redirect(url_for("index"))

    questions = Question.query.order_by(Question.time.desc()).all()
    flash("Hello to my word!")
    return render_template('index.html', questions=questions)#因为base模板中用到了moment的参数，所以这里要加一个返回current_time=datetime.now()的参数,但其主要目的是返回时间参数的数据,所以有了后面的queston参数作为返回的数据,前面的可以删除
#如果html有用到的数据必须在这里先进行返回，不然网页上是返回不了就读取不到相应的数据的questions=questions


@app.route('/questions')
def show_questions():
    questions = Question.query.all()
    for question in questions:
        print(question.name, question.time)  # 确认输出的时间是否正确
    return render_template('index.html', questions=questions)




if __name__ == '__main__':
    app.run()
