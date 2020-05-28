import os

import pymongo


def get_client(uri="mongodb://mongodb:27017"):
    """
    Return Pymongo client instance.

    Args:
        uri: Database connection URI

    """
    uri = os.environ.get("MONGO_URI", uri)
    return pymongo.MongoClient(uri)


def get_db(name="quickpickup"):
    """
    Return Pymongo client with database already selected.

    Args:
        name: Database name

    """
    client = get_client()
    db_name = os.environ.get("MONGO_DB_NAME", name)
    return client[db_name]


def collection(name):
    """
    Return Pymongo collection instance.

    Args:
        name: Collection name

    """
    db = get_db()
    coll = db[name]
    return coll
