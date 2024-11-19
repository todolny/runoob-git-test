from flask import Flask

import config

from exts import db
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.qa import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
#绑定配置文件
app.config.from_object(config)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

db.init_app(app)#在这里使db和app绑定

@app.route('/')
def hello_word():
    return "hello word"

if __name__ == '__main__':
    app.run()