from flask import Flask, g

import config

from exts import db, mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
#绑定配置文件
app.config.from_object(config)

db.init_app(app)#在这里使db和app绑定
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)



@app.route('/')
def hello_word():
    return "hello word"

@app.before_request
def my_before_request():


@app.context_processor
def my_context_processor():
    return {"user": g.user}

if __name__ == '__main__':
    app.run()