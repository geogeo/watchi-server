from pymongo import MongoClient
from config import MONGO_URI

_instance = None
def get_db():
    global _instance
    if _instance is None:
        _instance = MongoClient(MONGO_URI).watchi
    return _instance
