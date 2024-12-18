import random
import string

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session


from exts import mail, db
from flask_mail import Message
from models import EmailModel
from .forms import RegisterForm, LoginForm, ChangePasswordForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)#具体信息在LoginForm的表单当中
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

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


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
    if request.method == 'GET':
        return render_template("change_password.html")
    else:
        # form = LoginForm(request.form)  # 具体信息在LoginForm的表单当中
        form = ChangePasswordForm(request.form)
        if form.validate():
            email = form.email.data
            password_old = form.password_old.data#每个密码的名称索引的时候就要分开了，我还想着依次检查替代了
            password_new = form.password_new.data
            password_confirm = form.password_confirm.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("用户在数据库中不存在,请检查邮箱！")
                return redirect(url_for("auth.changePassword"))
            if check_password_hash(user.password, password_old):#其实这里是不知道原本的是返回的什么值，不过不能添加else的地步下只能先加个not试试了,
                user.password=generate_password_hash(password_confirm)#更改密码，这点我是一直在纠结着的，就是在那想怎么让二次的新密码直接确认相同能够直接表现出来，看现在的用法是直接替换了，相同还好，不同是不是直接页面报错？
                # db.session.add(user)   #居然是不要这个的，那提交的时候知道是往哪个数据库更新的吗，之后查一下，  因为上面指定了是user.password这个参数的值被替换掉的，所以不用在指定在哪个表里了
                db.session.commit()
                return redirect(url_for('auth.login'))
            # 验证用户提交的邮箱和验证码是否对应且正确
            # 表单的验证：flask-wtf:wtforms
            #都通过的话用注册表单的格式来提交新的信息，说是提交，修改应该是更恰当的，不知道方法是哪里有所改变，先试试基本的
            # form = Change_passwordForm(request.form)
            else:
                print(form.errors)
                return redirect(url_for("auth.changePassword"))
        else:
            print(form.errors)
            return redirect(url_for("auth.changePassword"))

@bp.route('/forgetPassword', methods=['GET', 'POST'])
def forgetPassword():
    if method == GET:
        return render_template(forgetPassword)

