from pymongo import MongoClient
from pymongo.server_api import ServerApi


class MongoDBConnection:
    """
    A class to manage MongoDB connections and handle collection retrieval.

    Attributes:
        MONGO_URI (str): The URI for connecting to the MongoDB server.
        DB_NAME (str): The name of the database to connect to.
        client (MongoClient): The MongoDB client instance.
        db (Database): The database instance.
        user_collection (Collection): The users collection.
        refresh_token_collection (Collection): The refresh tokens collection.
        user_session_collection (Collection): The user sessions collection.
        user_email_verification_token_collection (Collection): The user email verification tokens collection.
        book_collection (Collection): The books collection.
    """

    def __init__(self, MONGO_URI: str, DB_NAME: str):
        """
        Initialize the MongoDBConnection instance.

        Args:
            MONGO_URI (str): The URI for connecting to MongoDB.
            DB_NAME (str): The name of the database to connect to.

        Raises:
            ValueError: If MONGO_URI is not provided or is empty.
        """
        if not MONGO_URI:
            raise ValueError("MONGO_URI environment variable is not set or is empty.")
        
        self.MONGO_URI = MONGO_URI
        self.DB_NAME = DB_NAME
        self.client = None
        self.db = None

        # Initialize collection attributes
        self.user_collection = None
        self.refresh_token_collection = None
        self.user_session_collection = None
        self.user_email_verification_token_collection = None
        self.book_collection = None

    def start_connection(self):
        """
        Establish a connection to the MongoDB database and initialize collections.

        Raises:
            RuntimeError: If the connection to MongoDB fails.
        """
        try:
            self.client = MongoClient(self.MONGO_URI, server_api=ServerApi('1'))
            self.db = self.client[self.DB_NAME]
            
            # Initialize collections
            self.user_collection = self.db["users"]
            self.refresh_token_collection = self.db["refresh_tokens"]
            self.user_session_collection = self.db["user_sessions"]
            self.user_email_verification_token_collection = self.db["user_email_verification_tokens"]
            self.book_collection = self.db["books"]
            
            # Test the connection
            self.client.admin.command('ping')
            print(f"Successfully connected to MongoDB database: {self.DB_NAME}")
        except Exception as e:
            raise RuntimeError(f"Failed to connect to MongoDB: {e}")

    def get_collection(self, collection_name: str):
        """
        Retrieve a collection from the MongoDB database.

        Args:
            collection_name (str): The name of the collection to retrieve.

        Returns:
            Collection: The requested MongoDB collection.

        Raises:
            RuntimeError: If the database connection is not initialized.
        """
        if not self.db:
            raise RuntimeError("Database connection is not initialized. Call `start_connection` first.")
        
        return self.db[collection_name]

    def close_connection(self):
        """
        Close the connection to the MongoDB database.
        """
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")
