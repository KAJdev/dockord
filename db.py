import pymongo
import os

client = pymongo.MongoClient(os.environ.get('DOCKORD_MONGO'))

def get_user(id):
    return None

def update_user(id, update):
    return None

