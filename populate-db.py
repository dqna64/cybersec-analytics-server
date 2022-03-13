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

from pymongo import MongoClient
from pprint import pprint
import os

try:
    connection_str = os.environ["MONGODB_SECREVIEW_DB_CONN_STR"]
except KeyError:
    print(
        "Could not find env var MONGODB_SECREVIEW_DB_CONN_STR. Required to connect to MongoDB database."
    )
    raise

client = MongoClient(connection_str)
db = client.admin

serverStatusResult = db.command("serverStatus")

pprint(serverStatusResult)
