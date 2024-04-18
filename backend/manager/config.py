from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING', None)
MONGO_DB = os.getenv('MONGO_DB', None)
PORT = os.getenv('DESTINATION_MNG_PORT', None)
SOFT_LIST_URL = os.getenv('SOFT_LIST_URL', None)
WORKSPACE_MNG_URL = os.getenv('WORKSPACE_MNG_URL', None)

def get_database(tbl_name):
    if MONGO_CONNECTION_STRING is None:
        print("MONGO_CONNECTION_STRING is None")
        return None
    client = MongoClient(MONGO_CONNECTION_STRING)
    return client[tbl_name]
