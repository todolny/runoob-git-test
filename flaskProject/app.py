from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text#SQLAlchemy 的 execute 方法从 1.4 版本开始，要求执行的 SQL 必须是 sqlalchemy.text 对象（或 ORM 查询对象）。直接传字符串会导致 ObjectNotExecutableError
from flask_migrate import Migrate

import user

app = Flask(__name__)

HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "123456"
DATABASE = "database"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

#app.config中设置好连接数据库的信息
#然后使用SQLAchemy(app)创建一个db对象
#SQLAchemy会自动读取app.config中连接数据库的信息
db = SQLAlchemy(app)

migrate = Migrate(app, db)

#ORM模型映射成表的三步
#1.flask db init:这步只需要执行一次
#2.flask db migrate: 识别ORM模型的改变，生成迁移脚本
#3.flask db upgrade: 运行迁移脚本，同步到数据库中


# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text("select 1"))#要用text方法
#         print(rs.fetchone())

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #varchar,null=0
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))

class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    #添加作者的外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    #backref:会自动的给User模型添加一个articlers的属性，用来获取文章列表
    author = db.relationship("User", backref="articles")


# with app.app_context():
#     db.create_all()






@app.route('/')
def hello_world():
    user = User(username="大熊猫", email="120@qq.com")
    person = {
        "username": "食铁兽",
        "telephone": "157"
    }
    return render_template("blog.html", user=user, person=person)


@app.route("/user/add")
def add_user():
    try:
        user = User(username="芋圆", password="111")
        db.session.add(user)
        db.session.commit()
        return "用户创建成功！"
    except Exception as e:
        import traceback
        traceback.print_exc()  # 打印完整错误栈
        return f"创建用户失败，错误信息：{str(e)}"

@app.route("/user/query")
def query_user():
    #1.get查找：根据主键查找
    # user = User.query.get(1)
    # print(f"{user.id}: {user.username}--{user.password}")
    #2.filter_by查找
    #query:类数组
    users = User.query.filter_by(username="芋圆")
    for user in users:
        print(user.username)
    return "数据查找成功！"

@app.route("/user/update")
def update_user():
    user = User.query.filter_by(username="芋圆").first()
    user.password = "23456"
    db.session.commit()
    return "数据修改成功！"

@app.route("/user/delete")
def delete_user():
    user = User.query.get(1)
    db.session.delete(user)
    db.session.commit()
    return "数据删除成功！"


@app.route("/article/add")
def article_add():

    article1 = Article(title="Flask", content="学习大纲")
    article1.author = User.query.get(2)


    article2 = Article(title="Flask教程", content="初始")
    article2.author = User.query.get(2)
    db.session.add_all([article1, article2])
    db.session.commit()
    return "文章初成."

@app.route("/article/query")
def article_query():
    user = User.query.get(2)
    for article in user.articles:
        print(article.content)
    return "作者查询成功！"

@app.route("/filter")
def filter():
    user = User(username="了了", email="xx@qq.com")
    return render_template("filter.html",user=user)

@app.route("/control")
def control_statement():
    age = 17
    return render_template("control.html", age=age)

@app.route("/child1")
def child1():
    return render_template("child1.html")

@app.route("/child2")
def child2():
    return render_template("child2.html")

@app.route('/statics')
def statics():
    return render_template("static.html")

@app.route("/profiel")
def profile():
    return "大熊猫专场秀"

@app.route("/blog/name/<blog_name>")
def blog_name(blog_name):
    return render_template("blog.html",blog_name=blog_name)

@app.route('/book/page')
def book_page():
    page = request.args.get("page",default=1,type=int)
    return f"我想把人生翻到第{page}页"

if __name__ == '__main__':
    app.run(debug=True)
