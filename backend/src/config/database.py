# This file contains the MongoDBConnection class to handle MongoDB connection and collection retrieval.

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from src.config.env_setting import Config

class MongoDBConnection:
    """
    A class to handle MongoDB connection and collection retrieval.
    """
    def __init__(self, MONGO_URI: str, DB_NAME: str):
        if not MONGO_URI:
            raise ValueError("MONGO_URI environment variable is not set or is empty.")
        
        self.MONGO_URI = MONGO_URI
        self.DB_NAME = DB_NAME
        self.client = None
        self.db = None

    def start_connection(self):
        """
        Initialize the MongoDB connection.
        """
        try:
            # Initialize the MongoDB client
            self.client = MongoClient(self.MONGO_URI, server_api=ServerApi('1'))
            self.db = self.client[self.DB_NAME]  # Specify the database name
            # Create all the collections here
            self.user_collection = self.db["users"]
            self.user_email_verification_token_collection = self.db["user_email_verification_tokens"]

            # Test the connection
            self.client.admin.command('ping')
            print(f"Successfully connected to MongoDB database: {self.DB_NAME}")
        except Exception as e:
            print(f"Error during MongoDB connection: {e}")
            raise RuntimeError("Failed to connect to MongoDB.")

    def get_collection(self, collection_name: str):
        """
        Retrieve a collection from the database.
        
        :param collection_name: Name of the collection to retrieve.
        :return: The requested collection object.
        """
        if not self.db:
            raise RuntimeError("Database connection is not initialized. Call `start_connection` first.")
        
        return self.db[collection_name]

    def close_connection(self):
        """
        Close the MongoDB connection.
        """
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

# Instantiate the MongoDBConnection class
try:
    mongo_db_connection = MongoDBConnection(Config.MONGO_URI, Config.DB_NAME)
except Exception as e:
    print(f"Error: {str(e)}")
    raise e

