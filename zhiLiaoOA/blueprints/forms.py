import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailCaptchaModedl
from exts import db
#这些表单都是用来检查格式的
#注册的验证表单
class RegisterForm(wtforms.Form):
    email=wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    captcha=wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误")])
    username=wtforms.StringField(validators=[Length(min=4, max=20, message="用户名格式错误")])
    password=wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])
    password_confirm=wtforms.StringField(validators=[EqualTo("password")])

    #自定义验证
    #邮箱是否正确
    def validate_email(self, field):
        email=field.data
        user=UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError('该邮箱已被注册')

    # 验证码是否正确
    def validate_captcha(self,field):
        captcha=field.data
        email=self.email.data
        captcha_model=EmailCaptchaModedl.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message='邮箱或验证码错误')
        # else:
        #     db.session.delete(captcha_model)
        #     db.session.commit()

#用于修改密码的表单
class ChagnePasswordForm(wtforms.Form):
    email=wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    captcha=wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误")])
    password_old=wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])
    password_new = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])
    password_confirm=wtforms.StringField(validators=[EqualTo("password_new")])

    #自定义验证
    #邮箱是否正确
    def validate_email(self, field):
        email=field.data
        user=UserModel.query.filter_by(email=email).first()
        if not user:
            raise wtforms.ValidationError('没有该邮箱')

    # 验证码是否正确
    def validate_captcha(self,field):
        captcha=field.data
        email=self.email.data
        #数据库查询是否有邮箱和验证码这条数据
        captcha_model=EmailCaptchaModedl.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message='邮箱或验证码错误')

#登录的验证表单
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])

#用于验证问题的表单
class QuestionForm(wtforms.Form):
    title=wtforms.StringField(validators=[Length(min=3, max=100, message="标题格式错误")])
    content=wtforms.StringField(validators=[Length(min=3, message='内容格式错误')])

#发布回答的表单
class AnswerForm(wtforms.Form):
    content=wtforms.StringField(validators=[Length(min=3, message="内容格式错误！")])
    question_id=wtforms.IntegerField(validators=[InputRequired(message="必须要按传入整形id!")])