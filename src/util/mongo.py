from pymongo import MongoClient


def get_database(db_name):
    client = MongoClient("mongodb://root:s3cret@localhost:27017")
    return client[db_name]