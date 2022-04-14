import os
from pymongo import MongoClient
from exceptions import EnvVarException

DB_NAME = "secreview-db"
COLLECN_NAME = "cybersec-incidents-collecn"
DATA_PATH = "../VCDB/data/json/validated/"


def load_db(func):
    def wrapper():
        connection_str = os.environ.get("MONGODB_SECREVIEW_CONNSTR")

        if connection_str is None:
            raise EnvVarException(
                "Could not find env var MONGODB_SECREVIEW_CONNSTR. Required to connect to MongoDB database."
            )

        client = MongoClient(connection_str)
        db = client[DB_NAME]
        collecn = db[COLLECN_NAME]

        return func(collecn)

    return wrapper
