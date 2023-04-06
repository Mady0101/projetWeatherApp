import pymongo

client = pymongo.MongoClient("mongodb://root:example@mongo:27017/")
db = client["mydatabase"]

def get_instance_db():
    if db is None:
        client = pymongo.MongoClient("mongodb://root:example@mongo:27017/")
        db = client["mydatabase"]
    return db