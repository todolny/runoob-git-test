import random
import string

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session


from exts import mail, db
from flask_mail import Message
from models import EmailModel
from .forms import RegisterForm, LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在！")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):
                #cookie
                #cookie中不适合存储太多的数据，只适合存储少量的数据
                #cookie中一般用来存放登录授权的东西
                #flask中的session，是经过加密后存储在cookie中的
                session['user_id'] = user.id
                return redirect("/")
            else:
                print("密码错误！")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))






@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    # 如果刚开始环境没有配好，不能自动出来flask的设置文件夹的话，一些目录路径还需要自己再进行手动的配置
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单的验证：flas-wtf:wtforms
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))


@bp.route("/captcha/email")
def get_captcha():
    email = request.args.get("email")
    source = string.digits * 4
    captcha: object = random.sample(source, 4)
    captcha = "".join(captcha)
    message = Message(subject="大熊猫基地注册验证码", recipients=[email], body=f"您的验证码是：{captcha}")
    mail.send(message)
    # memcached/redis
    # 用数据库的方式存储
    email_captcha = EmailModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # RESTFUL API
    # {code:200/400/500,message:"",data: {}}

    return jsonify({"code": 200, "message": "", "data": None})


@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试", recipients=["1207840645@qq.com"], body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功！"


@bp.route('/changePassword', methods=['GET', 'POST'])
def changePassword():
    return "世道维艰"
