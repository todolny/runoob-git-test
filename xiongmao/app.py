from flask import Flask, g, session

import config

from exts import db, mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
#绑定配置文件
app.config.from_object(config)

db.init_app(app)#在这里使db和app绑定，绑定数据库
mail.init_app(app)#绑定邮箱

migrate = Migrate(app, db)#第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例，创建数据库迁移工具对象


app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)



#钩子函数在 Flask 应用程序中，请求钩子（Request Hooks）是一种强大的机制，它允许我们在请求的不同阶段插入自定义的代码。这些钩子函数可以用于在处理请求之前或之后执行特定的操作，如验证请求、记录日志、设置上下文等。
@app.before_request#在每次请求之前执行。这个钩子函数可以用来给视图函数增加一些变量。请求已经到达 Flask，但还没有进入具体的视图函数之前调用。您可以在这里处理一些后续需要用到的数据，方便视图函数使用。
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)#真的是很小的一个错误，get(user_id)中的参数user_id是不带双引号的，之前带的有所以一直导致判断user为空
        setattr(g, "user", user)#在 Flask 应用程序中，setattr() 函数是一个强大的工具，用于在运行时动态设置对象的属性。g是全局变量
    else:
        setattr(g, "user", None)


@app.context_processor#上下文，在所有模板中(html文件)都可以访问这里创建的属性
def my_context_processor():
    return {"user": g.user}

if __name__ == '__main__':
    app.run()