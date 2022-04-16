"""
Run serve by:
$ python -m server
"""

from collections import defaultdict
from flask import Flask
import json
from loadCollecn import load_collecn
from bson import json_util
from random import shuffle
from markupsafe import escape
from pprint import pprint

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


@app.route("/incidents/<int:limit>", methods=["GET"])
def get_incidents(limit):
    """
    Returns a list of documents in incidents_collecn. Limited to <limit> num of docs.
    """
    if incidents_collecn is None:
        print(f"Cybersec incidents collection not yet loaded.")
        return json.dumps({})
    result = list(incidents_collecn.find())
    shuffle(result)
    if len(result) > limit:
        result = result[:limit]
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


@app.route("/overview", methods=["GET"])
def get_overview():
    if incidents_collecn is None:
        print(f"Cybersec incidents collection not yet loaded.")
        return json.dumps({})
    total_num_docs = incidents_collecn.count_documents()
    return json.dumps({"total_num_incidents": total_num_docs})


@app.route("/actor_types_and_varieties", methods=["GET"])
def get_actor_types_and_varieties():
    """
    Gets count of each actor type and variety in the form:
    {
        "external": {
            "activist": int,
            "competitor": int,
            "Organized crime": int,
            ...
        },
        "internal": {
            "cashier": int,
            "End-user": int,
            "Maintenance": int,
            ...
        },
        "partner": int,
    }
    Note that each incident can have multiple types and varieties of actors.
    """
    if incidents_collecn is None:
        print(f"Cybersec incidents collection not yet loaded.")
        return json.dumps({})
    docs = incidents_collecn.find()
    result = {"external": defaultdict(int), "internal": defaultdict(int), "partner": 0}
    for doc in docs:
        ## `actor` and `variety` are required, no need to check for existence.
        if "external" in doc["actor"]:
            varieties = doc["actor"]["external"]["variety"]
            for variety in varieties:
                result["external"][variety] += 1
        if "internal" in doc["actor"]:
            varieties = doc["actor"]["internal"]["variety"]
            for variety in varieties:
                result["internal"][variety] += 1
        if "partner" in doc["actor"]:
            result["partner"] += 1

    return json.dumps(result)


@app.route("/actor_motives", methods=["GET"])
def get_actor_motives():
    """
    Gets count of each actor motive.
    """
    if incidents_collecn is None:
        print(f"Cybersec incidents collection not yet loaded.")
        return json.dumps({})
    if schemas_collecn is None:
        print(f"Schemas collection not yet loaded.")
        return json.dumps({})

    vcdb_enum = schemas_collecn.find_one({"schema_name": "vcdb_enum"})
    ## Get set of keys from external, internal and partner motives (they should
    # be the same, but this is just to be safe).
    keys = set.union(
        set(vcdb_enum["actor"]["external"]["motive"]),
        set(vcdb_enum["actor"]["internal"]["motive"]),
        set(vcdb_enum["actor"]["partner"]["motive"]),
    )
    result = dict.fromkeys(keys, 0)

    docs = incidents_collecn.find()
    for doc in docs:
        if "external" in doc["actor"]:
            motives = doc["actor"]["external"]["motive"]
            for motive in motives:
                result[motive] += 1
        if "internal" in doc["actor"]:
            motives = doc["actor"]["internal"]["motive"]
            for motive in motives:
                result[motive] += 1
        if "partner" in doc["actor"]:
            motives = doc["actor"]["partner"]["motive"]
            for motive in motives:
                result[motive] += 1

    return json.dumps(result)


@app.route("/actor_countries", methods=["GET"])
def get_actor_countries():
    """
    Gets count of each actor country.
    """
    if incidents_collecn is None:
        print(f"Cybersec incidents collection not yet loaded.")
        return json.dumps({})
    if schemas_collecn is None:
        print(f"Schemas collection not yet loaded.")
        return json.dumps({})

    vcdb_enum = schemas_collecn.find_one({"schema_name": "vcdb_enum"})
    ## Get set of keys from external, internal and partner countries (they should
    # be the same, but this is just to be safe).
    keys = set.union(
        set(vcdb_enum["actor"]["external"]["country"]),
        set(vcdb_enum["actor"]["partner"]["country"]),
        set(vcdb_enum["victim"]["country"]),
    )
    result = dict.fromkeys(keys, 0)

    docs = incidents_collecn.find()
    for doc in docs:
        if "external" in doc["actor"] and "country" in doc["actor"]["external"]:
            countries = doc["actor"]["external"]["country"]
            for country in countries:
                result[country] += 1
        if "partner" in doc["actor"] and "country" in doc["actor"]["partner"]:
            countries = doc["actor"]["partner"]["country"]
            for country in countries:
                result[country] += 1
        if "internal" in doc["actor"]:
            countries = doc["victim"]["country"]  ## Both guaranteed.
            for country in countries:
                result[country] += 1

    return json.dumps(result)


@app.route("/action_types_and_varieties", methods=["GET"])
def get_action_types_and_varieties():
    """
    Gets count of each action type and variety.
    """
    if incidents_collecn is None:
        print(f"Cybersec incidents collection not yet loaded.")
        return json.dumps({})
    if schemas_collecn is None:
        print(f"Schemas collection not yet loaded.")
        return json.dumps({})

    vcdb_enum = schemas_collecn.find_one({"schema_name": "vcdb_enum"})
    type_keys = set(vcdb_enum["action"].keys())
    result = {}
    for type_key in type_keys:
        if type_key != "unknown":
            result[type_key] = {}
            ## Varieties for this action type
            variety_keys = vcdb_enum["action"][type_key]["variety"]
            for variety_key in variety_keys:
                result[type_key][variety_key] = 0
        else:
            result[type_key] = 0

    docs = incidents_collecn.find()
    for doc in docs:
        for type, val in doc["action"].items():
            ## 'variety' not present in type 'unknown'
            if type != "unknown":
                for variety in val["variety"]:
                    result[type][variety] += 1
            else:
                result[type] += 1

    return json.dumps(result)


@app.route("/action_types_and_vectors", methods=["GET"])
def get_action_types_and_vectors():
    """
    Gets count of each action type and vector.
    """
    if incidents_collecn is None:
        print(f"Cybersec incidents collection not yet loaded.")
        return json.dumps({})
    if schemas_collecn is None:
        print(f"Schemas collection not yet loaded.")
        return json.dumps({})

    vcdb_enum = schemas_collecn.find_one({"schema_name": "vcdb_enum"})
    type_keys = set(vcdb_enum["action"].keys())
    result = {}
    for type_key in type_keys:
        if type_key not in ("unknown", "environmental"):
            ## default dict bc some vector keys in documents are missing from enum
            result[type_key] = defaultdict(int)
            ## Varieties for this action type
            vector_keys = vcdb_enum["action"][type_key]["vector"]
            for vector_key in vector_keys:
                result[type_key][vector_key] = 0
        else:
            result[type_key] = 0

    docs = incidents_collecn.find()
    for doc in docs:
        for type, val in doc["action"].items():
            ## 'vector' not present in type 'unknown' or 'environmental'
            if type not in ("unknown", "environmental"):
                for vector in val["vector"]:
                    result[type][vector] += 1
            else:
                result[type] += 1

    return json.dumps(result)


if __name__ == "__main__":
    incidents_collecn = load_collecn(DB_NAME, INCIDENTS_COLLECN_NAME)
    schemas_collecn = load_collecn(DB_NAME, SCHEMAS_COLLECN_NAME)
    app.run(port=5000)
