from flask import Flask, render_template, session, g
from exts import db, mail, jwt
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate
from flask import request




app=Flask(__name__)#确定程序的根目录，，以便获得静态文件（static的js、css、jquery）和模板文件（tempates的html）

print(app.name)

app.config.from_object('config')#配置文件，里面有数据库和邮件发送的相关配置

db.init_app(app)#数据库初始化
mail.init_app(app)#邮箱初始化
jwt.init_app(app)#jwt初始化

migrate=Migrate(app,db)#数据库迁移

#注册蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

#钩子函数在 Flask 应用程序中，请求钩子（Request Hooks）是一种强大的机制，它允许我们在请求的不同阶段插入自定义的代码。这些钩子函数可以用于在处理请求之前或之后执行特定的操作，如验证请求、记录日志、设置上下文等。
@app.before_request#在每次请求之前执行。这个钩子函数可以用来给视图函数增加一些变量。请求已经到达 Flask，但还没有进入具体的视图函数之前调用。您可以在这里处理一些后续需要用到的数据，方便视图函数使用。
def my_before_request():
    user_id=session.get("user_id")
    if user_id:
        user=UserModel.query.get(user_id)
        setattr(g,"user",user)#在 Flask 应用程序中，setattr() 函数是一个强大的工具，用于在运行时动态设置对象的属性。
    else:
        setattr(g,"user",None)

@app.context_processor#上下文，在所有模板中(html文件)都可以访问这里创建的属性
def my_context_processor():
    return {"user":g.user}


if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)