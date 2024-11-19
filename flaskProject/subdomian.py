from flask import Flask, g

app = Flask(__name__)

@app.url_value_preprocessor
def get_site(endpoint, values):
    if values is not None:
        g.site = values.pop('subdomain', None)

@app.route('/', subdomain='<subdomain>')
def index():
    return g.site or "No subdomain"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
