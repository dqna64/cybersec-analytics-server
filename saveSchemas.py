from pymongo import MongoClient
from pprint import pprint
import os
import json
from exceptions import EnvVarException
from loadCollecn import load_collecn

DB_NAME = "secreview-db"
COLLECN_NAME = "schemas-collecn"
DATA_PATH = "../VCDB/"


def save_vcdb_merged_schema(collecn):
    file_name = "vcdb-merged.json"
    fd = open(os.path.join(DATA_PATH, file_name))

    merged_schema = None
    try:
        merged_schema = json.load(fd)
    except Exception as err:
        print(f"Could not deserialise fd of file name {file_name}")
        raise err

    schema_name = "vcdb_merged"
    del merged_schema["$schema"]
    merged_schema["schema_name"] = schema_name

    try:
        collecn.replace_one({"schema_name": schema_name}, merged_schema, upsert=True)
        print(f"Schema {schema_name} in collection {COLLECN_NAME} has been replaced.")
    except Exception as err:
        print(
            f"Schema {schema_name} in collection {COLLECN_NAME} could not be replaced."
        )
        raise err

    return merged_schema


if __name__ == "__main__":
    collecn = load_collecn(DB_NAME, COLLECN_NAME)
    save_vcdb_merged_schema(collecn)
