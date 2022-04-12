from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "<p>Greetings world!</p>"


if __name__ == "__main__":
    print(__name__)
