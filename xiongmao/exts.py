#exts.py：这个文件存在的目的就是为了解决循环引用

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()