import string
from exts import db
from flask import Blueprint,render_template,jsonify, redirect, url_for, session
from exts import mail
from flask_mail import Message
from flask import request
import random
from models import EmailCaptchaModedl
from .forms import RegisterForm, LoginForm, ChagnePasswordForm
from  models import UserModel
from  werkzeug.security import generate_password_hash, check_password_hash #用来加密密码
from flask_jwt_extended import create_access_token#用来创建jwt的token
#使前缀都要加上/auth
bp=Blueprint('auth',__name__,url_prefix='/auth')

#登录界面的路由
@bp.route('/login',methods=["POST","GET"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        #获取表单
        form=LoginForm(request.form)
        #判断表单格式
        if form.validate():#正确则开始跟数据库里的数据进行验证
            email=form.email.data#data是字段的值
            password=form.password.data
            user=UserModel.query.filter_by(email=email).first()
            if not user:
                print("用户在数据库中不存在")
                return  redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):#如果密码正确，返回session
                #创建一个token
                access_token = create_access_token(identity=user.id)
                session['user_id']=user.id
                return redirect("/")
            else:#不正确则进行返回
                print(form.errors)
                return redirect(url_for("auth.login"))
        else:  # 不正确则进行返回
            print(form.errors)
            return redirect(url_for("auth.login"))


#注册的界面
@bp.route('/register',methods=['GET', 'POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        #把前端给的表单进行验证
        form=RegisterForm(request.form)
        #自动调用验证器以及自己定义的验证
        if form.validate():#通过验证后把数据加入到数据库中
            email=form.email.data
            username=form.username.data
            password=form.password.data
            user=UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            #跳转到登录页面
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            #重新返回注册页面
            return redirect(url_for('auth.register'))

#生成邮箱注册码、发送邮箱注册码并存入数据库,如果没有指定methods参数，默认就是GET请求
@bp.route('/captcha/email')
def get_email_captcha():
    #当get请求时，需要使用request.args来获取数据,URL请求参数
    email=request.args.get("email")#request 是一个对象，它代表了客户端发来的 HTTP 请求。args 是一个字典，包含了请求中的查询参数（例如 URL 中的查询字符串）。get("email") 是一个方法，用于从查询参数中获取名为 “email” 的值。如果查询参数中没有 “email”，则返回 None。
    #生成随机数并变成字符串
    source=string.digits*4
    captcha=random.sample(source,4)
    captcha="".join(captcha)
    #生成邮件，发送邮件
    message = Message(subject="flask学习验证码", recipients=[email], body=f"您的验证码是{captcha}")
    mail.send(message)
    #先检查下数据库里是否有这个邮箱的验证码
    email_c=EmailCaptchaModedl.query.filter_by(email=email).first()
    if not email_c:#如果没有
        #将邮箱和验证码都存储到数据库中
        email_captcha=EmailCaptchaModedl(email=email,captcha=captcha)
        db.session.add(email_captcha)
        db.session.commit()
    else:#如果有则将其验证码进行更改
        email_c.captcha=captcha
        db.session.commit()
    print(captcha)
    #返回json格式的数据
    #{code:200(正常)/400(客户端错误)/500(服务器错误),messqge：""(如果错误的话错误信息), data：""}
    return jsonify({"code":200, "message":"", "data":None})

#邮箱测试
@bp.route('/mail/test')
def mail_test():
    message=Message(subject="邮箱测试", recipients=["1642992358@qq.com"],body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功"

#修改密码的页面
@bp.route('/changePassword',methods=['GET', 'POST'])
def changePassword():
    if request.method=='GET':
        return render_template('change_password.html')
    else:
        #把前端给的表单进行验证
        form=ChagnePasswordForm(request.form)
        #自动调用验证器以及自己定义的验证
        if form.validate():#通过验证后把数据加入到数据库中
            email = form.email.data  # data是字段的值
            password_old = form.password_old.data
            password_new=form.password_new.data
            password_confirm=form.password_confirm.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("用户在数据库中不存在")
                return redirect(url_for("auth.changePassword"))
            if check_password_hash(user.password, password_old):#检查原先密码是否正确
                user.password=generate_password_hash(password_confirm)#更改密码
                db.session.commit()
                return redirect(url_for('auth.login'))
            else:  # 不正确则进行返回
                print(form.errors)
                return redirect(url_for("auth.changePassword"))
        else:
            print(form.errors)
            #重新返回注册页面
            return redirect(url_for('auth.changePassword'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect("/")