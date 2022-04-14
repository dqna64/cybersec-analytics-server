from pprint import pprint
import os
import json
from loadCollecn import load_collecn

DB_NAME = "secreview-db"
COLLECN_NAME = "cybersec-incidents-collecn"
DATA_PATH = "../VCDB/data/json/validated/"


def populate_db(collecn):

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


def query1(collecn):
    print(
        f"Number of documents in collection '{collecn.name}': {collecn.count_documents({})}"
    )
    for doc in collecn.find():
        # pprint(doc)
        break


if __name__ == "__main__":
    collecn = load_collecn(DB_NAME, COLLECN_NAME)
    populate_db(collecn)
