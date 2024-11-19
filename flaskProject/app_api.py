from flask import Flask,jsonify,url_for
from flask.views import MethodView

app = Flask(__name__)

class UserAPI(MethodView):
    def get(self):
        avatar_url = url_for('static', filename='images/R-C.jpg')
        return jsonify({
            'username': 'fake',
            'avatar': 'avatar_url'
        })
    def post(self):
        return 'UNSUPPORTED'

app.add_url_rule('/user',view_func=UserAPI.as_view('userview'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000)

def user_required(f):
    def decorator(*args,**kwargs):
        if not g.user:
            abort(401)
        return f(*args,**kwargs)
    return decorator

view = user_required(UserAPI.as_view('users'))
app.add_url_rule('/uesrs/',view_func=view)

class UserAPI(MethodView):
    decorators = [user_required]