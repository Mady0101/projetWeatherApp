
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["capitales"]
recherche = db["recherche"]
loc=db["localisation"]