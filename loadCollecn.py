import os
from pprint import pprint
from pymongo import MongoClient
from exceptions import EnvVarException


def load_collecn(db_name, collecn_name):
    connection_str = os.environ.get("MONGODB_SECREVIEW_CONNSTR")
    if connection_str is None:
        raise EnvVarException(
            "Could not find env var MONGODB_SECREVIEW_CONNSTR. Required to connect to MongoDB database."
        )

    client = MongoClient(connection_str)
    db = client[db_name]
    collecn = db[collecn_name]

    serverStatusResult = db.command("serverStatus")
    # pprint(serverStatusResult)
    print(f"Successfully loaded collection {collecn.name} from database {db.name}.")
    print(f"Collections in db '{db_name}': {db.list_collection_names()}")

    return collecn
