from flask import Flask,request,abort,redirect,url_for

app = Flask(__name__)
app.config.from_object('config')

@app.route('/people/')
def people():
    name = request.args.get('name')
    if not name:
        return redirect(url_for('login'))
    user_agent = request.headers.get('User-Agent')
    return 'Name: {0}; UA: {1}'.format(name,user_agent)

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('uesr_id')
        return 'User: {} login'.format(user_id)
    else:
        return 'Open Login page'

@app.route('/secret/')
def secret():
    abort(401)
    print('this is never executed')

if __name__ == '__main__':
    app.run(host='192.168.30.236',port=8080,debug=app.debug)