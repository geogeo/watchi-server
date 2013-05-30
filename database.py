from pymongo import MongoClient
import config

_instance = None
def get_db():
    global _instance
    if _instance is None:
        _instance = MongoClient(config.MONGO_URI).watchi
    return _instance
