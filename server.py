from flask import Flask
import json
from loadDbDec import load_db
from bson import json_util
from random import shuffle

MAX_DOCS_DUMP = 1200

app = Flask(__name__)


@app.route("/")
def hello():
    return "<p>Greetings world!</p>"


@app.route("/all-incidents", methods=["GET"])
@load_db
def get_all_incidents(collecn):
    """
    Returns a list of all documents in collection.
    """
    result = list(collecn.find())
    shuffle(result)  ## In-place shuffle
    if len(result) > MAX_DOCS_DUMP:
        result = result[:MAX_DOCS_DUMP]
    return json.dumps(result, default=json_util.default)


if __name__ == "__main__":
    print(__name__)
