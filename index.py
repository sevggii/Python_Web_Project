from flask import Flask

app = Flask(__name__)

@app.route('/')
def ana_sayfa():
    return 'Hello, Flask!'
