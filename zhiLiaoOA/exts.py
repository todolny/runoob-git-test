#这个文件就是为了解决循环引用
#用到的插件都放这里
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_jwt_extended import  JWTManager

db = SQLAlchemy()
mail=Mail()
jwt=JWTManager()