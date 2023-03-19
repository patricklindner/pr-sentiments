from flask import Flask

app = Flask(__name__)


@app.get("/")
def hello():
    return "<h1>Hello Flask</h1>"
