from flask import Flask, request, render_template
from flask.views import View

app = Flask(__name__, template_folder='templates')

class BaseView(View):
    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        if request.method != 'GET':
            return 'UNSUPPORTED!'

class UserView(BaseView):
    def get_template_name(self):
        return 'chapter3/section1/users.html'

    def get_users(self):
        return [{
            'username': 'fake',
            'avatar': 'http://lorempixel.com/100/100/nature'
        }]

    def dispatch_request(self):
        print("Dispatching request")
        if request.method == 'GET':
            users = self.get_users()
            return self.render_template({'users': users})
        return 'UNSUPPORTED!'

app.add_url_rule('/users', view_func=UserView.as_view('userview'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001)
