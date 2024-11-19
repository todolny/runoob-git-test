from flask import Flask, url_for

app = Flask(__name__)

@app.route('/item/<int:id>/')
def item(id):
    return f'Item ID: {id}'

@app.route('/test-url/')
def test_url():
    # 使用 url_for 生成 URL
    item_url = url_for('item', id=2, next='/')
    return f'The URL is: {item_url}'

if __name__ == '__main__':
    app.run(debug=True)
