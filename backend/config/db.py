from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

MONGO_URI = os.getenv("MONGO_URI")

# Send a ping to confirm a successful connection
try:
    # Create a new client and connect to the server
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))  # server_api=ServerApi('1') is required for MongoDB 5.0
    db = client.FastAPICRUDDB
    collection = db["user"]
    collection2 = db["product"]
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(e)


