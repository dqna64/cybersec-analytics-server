from pymongo import MongoClient
from pprint import pprint
import os
import json
from exceptions import EnvVarException
from loadCollecn import load_collecn

DB_NAME = "secreview-db"
SCHEMAS_COLLECN_NAME = "schemas-collecn"
ISO3166_COLLECN_NAME = "iso3166-collecn"
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
        print(
            f"Schema {schema_name} in collection {SCHEMAS_COLLECN_NAME} has been replaced."
        )
    except Exception as err:
        print(
            f"Schema {schema_name} in collection {SCHEMAS_COLLECN_NAME} could not be replaced."
        )
        raise err

    return merged_schema


def save_vcdb_enum(collecn):
    file_name = "vcdb-enum.json"
    fd = open(os.path.join(DATA_PATH, file_name))

    merged_enum = None
    try:
        merged_enum = json.load(fd)
    except Exception as err:
        print(f"Could not deserialise fd of file name {file_name}")
        raise err

    schema_name = "vcdb_enum"
    merged_enum["schema_name"] = schema_name

    try:
        collecn.replace_one({"schema_name": schema_name}, merged_enum, upsert=True)
        print(
            f"Enum {schema_name} in collection {SCHEMAS_COLLECN_NAME} has been replaced."
        )
    except Exception as err:
        print(
            f"Enum {schema_name} in collection {SCHEMAS_COLLECN_NAME} could not be replaced."
        )
        raise err

    return merged_enum


def save_iso_3166(collecn):
    file_name = "iso3166.json"
    fd = open(os.path.join(DATA_PATH, file_name))

    iso3166_data = None
    try:
        iso3166_data = json.load(fd)
    except Exception as err:
        print(f"Could not deserialise fd of file name {file_name}")
        raise err

    for country in iso3166_data:
        try:
            collecn.replace_one({"name": country["name"]}, country, upsert=True)
            print(
                f"Doc {country['name']} in collection {ISO3166_COLLECN_NAME} has been replaced."
            )
        except Exception as err:
            print(
                f"Doc {country['name']} in collection {ISO3166_COLLECN_NAME} could not be replaced."
            )
            raise err

    return iso3166_data


if __name__ == "__main__":
    schemas_collecn = load_collecn(DB_NAME, SCHEMAS_COLLECN_NAME)
    # save_vcdb_merged_schema(schemas_collecn)
    # save_vcdb_enum(schemas_collecn)

    iso3166_collecn = load_collecn(DB_NAME, ISO3166_COLLECN_NAME)
    save_iso_3166(iso3166_collecn)
