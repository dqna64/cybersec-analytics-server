"""
Run serve by:
$ python -m server
"""

from flask import Flask
import json
from loadCollecn import load_collecn
from loadDbDec import COLLECN_NAME, load_db
from bson import json_util
from random import shuffle

MAX_DOCS_DUMP = 1200
DB_NAME = "secreview-db"
INCIDENTS_COLLECN_NAME = "cybersec-incidents-collecn"
SCHEMAS_COLLECN_NAME = "schemas-collecn"


app = Flask(__name__)

incidents_collecn = None
schemas_collecn = None


@app.route("/")
def hello():
    return "<p>Greetings world!</p>"


@app.route("/all-incidents", methods=["GET"])
def get_all_incidents():
    """
    Returns a list of all documents in collection.
    """
    if incidents_collecn is None:
        print(f"Cybersec incidents collection not yet loaded.")
        return json.dumps({})
    result = list(incidents_collecn.find())
    shuffle(result)  ## In-place shuffle
    if len(result) > MAX_DOCS_DUMP:
        result = result[:MAX_DOCS_DUMP]
    return json.dumps(result, default=json_util.default)


@app.route("/schema", methods=["GET"])
def get_schema():
    """
    Returns vcdb merged schema.
    """
    if schemas_collecn is None:
        print(f"Schemas collection not yet loaded.")
        return json.dumps({})
    result = schemas_collecn.find_one({"schema_name": "vcdb_merged"})
    return json.dumps(result, default=json_util.default)


if __name__ == "__main__":
    incidents_collecn = load_collecn(DB_NAME, INCIDENTS_COLLECN_NAME)
    schemas_collecn = load_collecn(DB_NAME, SCHEMAS_COLLECN_NAME)
    app.run(port=5000)
