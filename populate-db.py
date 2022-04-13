# import pymongo
# import json
# import os

# SERVER = "localhost"
# DATABASE = "kevin"
# COLLECTION = "vcdb"

# server = pymongo.Connection(SERVER)
# server.drop_database(DATABASE)
# db = server[DATABASE]
# col = db[COLLECTION]


# for (path, dirs, files) in os.walk("../data/json/"):
#     for file in files:
#         print("loading: " + os.path.join("../data/json/", file))
#         infile = open(os.path.join("../data/json/", file), "rb")
#         incident = json.loads(infile.read())
#         col.insert(incident)

from cmath import log
from pymongo import MongoClient
from pprint import pprint
import os
import json
from exceptions import EnvVarException


def populate_db():
    connection_str = os.environ.get("MONGODB_SECREVIEW_CONNSTR")
    if connection_str is None:
        raise EnvVarException(
            "Could not find env var MONGODB_SECREVIEW_CONNSTR. Required to connect to MongoDB database."
        )

    client = MongoClient(connection_str)
    db = client[DB_NAME]
    # collection = client[COLLECN_NAME]
    collecn = db[COLLECN_NAME]

    serverStatusResult = db.command("serverStatus")

    pprint(serverStatusResult)

    print(f"Collections in db '{DB_NAME}': {db.list_collection_names()}")

    try:
        (_, _, file_names) = next(os.walk(DATA_PATH))
    except StopIteration:
        print(f"Iterator of os.walk('{DATA_PATH}') is empty")
        file_names = []

    for file_name in file_names:
        try:
            f = open(os.path.join(DATA_PATH, file_name))
        except FileNotFoundError as err:
            print(err)
            print(f"file_name: {file_name}")
            continue

        try:
            incident_data = json.load(f)
        except Exception as err:
            print(err)
            print(f"Could not deserialise fd of file name {file_name}")
            continue
        find_result = collecn.find_one({"incident_id": incident_data["incident_id"]})
        if find_result is None:
            print(
                f"Incident with id {incident_data['incident_id']} not found in collection {COLLECN_NAME}, inserting."
            )
            collecn.insert_one(incident_data)
        else:
            print(
                f"Incident with id {incident_data['incident_id']} already exists in collection {COLLECN_NAME}."
            )


if __name__ == "__main__":
    DB_NAME = "secreview-db"
    COLLECN_NAME = "cybersec-incidents-collecn"
    DATA_PATH = "../VCDB/data/json/validated/"
    populate_db()
