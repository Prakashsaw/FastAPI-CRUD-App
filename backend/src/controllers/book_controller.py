# Books controller class which provide the CRUD operations for the books.
from fastapi import HTTPException, status
from typing import List
from fastapi.responses import JSONResponse
from datetime import datetime
from src.config.database import MongoDBConnection
from src.utils.generate_unique_key import generate_unique_key
from src.serializers.book_serializer import book_data, all_books_data
from src.config.env_setting import Settings

class BookControllersClass:
    # Add book controller
    async def add_book_controller(self, data: dict, user_id: str) -> dict:
        """
        Add book controller.
        """
        try:
            Config = Settings()
            mongo_db_connection = MongoDBConnection(Config.MONGO_URI, Config.DB_NAME)

            add_payload = {}
            # Add the user_id to the payload
            unique_id = generate_unique_key()

            created_at = str(datetime.now())
            updated_at = str(datetime.now())

            add_payload["user_id"] = user_id
            add_payload["book_id"] = unique_id
            add_payload["category"] = data.get("category")
            add_payload["book_title"] = data.get("book_title")
            add_payload["book_author"] = data.get("book_author")
            add_payload["book_price"] = data.get("book_price")
            add_payload["publisher"] = data.get("publisher")
            add_payload["published_date"] = data.get("published_date")
            add_payload["page_count"] = data.get("page_count")
            add_payload["language"] = data.get("language")
            add_payload["book_rating"] = data.get("book_rating")
            add_payload["book_image"] = data.get("book_image")
            add_payload["created_at"] = created_at
            add_payload["updated_at"] = updated_at

            # print("add_payload: ", add_payload)

            # Start the connection and get the book collection
            mongo_db_connection.start_connection()
            book_collection = mongo_db_connection.get_collection("books")
            res = book_collection.insert_one(add_payload)
            if res.inserted_id:
                # find the inserted book and return it
                inserted_book = book_collection.find_one({"book_id": unique_id})
                if inserted_book:
                    selialized_inserted_book = book_data(inserted_book)
                    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"status":"success", "message":"Book added successfully.", "book":selialized_inserted_book})
                else:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get inserted book" )
                
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add book" )
            
        except Exception as e:
            raise e
        finally:
            # Close the connection
            mongo_db_connection.close_connection()
            
    # Get all books controller
    async def get_all_books_controller(self, user_id: str) -> List[dict]:
        """
        Get all books controller.
        """
        try:
            Config = Settings()
            mongo_db_connection = MongoDBConnection(Config.MONGO_URI, Config.DB_NAME)

            # Start the connection and get the book collection
            mongo_db_connection.start_connection()
            book_collection = mongo_db_connection.get_collection("books")
            all_books = book_collection.find({"user_id": user_id})
            if all_books:
                serialized_books = all_books_data(all_books)
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status":"success", "message":"All the books fetched successfully.", "books":serialized_books})
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found")
        except Exception as e:
            raise e
        finally:
            # Close the connection
            mongo_db_connection.close_connection()

    # Get book by ID controller to current logged In user
    async def get_book_by_id_controller(self, user_id: str, book_id: str) -> dict:
        """
        Get book by ID controller.
        """
        try:
            Config = Settings()
            mongo_db_connection = MongoDBConnection(Config.MONGO_URI, Config.DB_NAME)

            # Start the connection and get the book collection
            mongo_db_connection.start_connection()
            book_collection = mongo_db_connection.get_collection("books")
            book = book_collection.find_one({"user_id": user_id, "book_id": book_id})
            if book:
                serialized_book = book_data(book)
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status":"success", "message":"Book fetched successfully.", "book":serialized_book})
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No book found")
        except Exception as e:
            raise e
        finally:
            # Close the connection
            mongo_db_connection.close_connection()

    # Update book controller
    async def update_book_controller(self, update_payload: dict, user_id: str, book_id: str) -> dict:
        """
        Update book controller.
        """
        try:
            Config = Settings()
            mongo_db_connection = MongoDBConnection(Config.MONGO_URI, Config.DB_NAME)

            # Start the connection and get the book collection
            mongo_db_connection.start_connection()
            book_collection = mongo_db_connection.get_collection("books")
            updated_at = str(datetime.now())
            update_payload["updated_at"] = updated_at
            update_res = book_collection.update_one({"user_id": user_id, "book_id": book_id}, {"$set": update_payload})
            if update_res.modified_count:
                updated_book = book_collection.find_one({"user_id": user_id, "book_id": book_id})
                if updated_book:
                    serialized_updated_book = book_data(updated_book)
                    return JSONResponse(status_code=status.HTTP_200_OK, content={"status":"success", "message":"Book updated successfully.", "book":serialized_updated_book})
                else:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get updated book" )
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to update book! Book with this book_id doesn't exist." )
        except Exception as e:
            raise e
        finally:
            # Close the connection
            mongo_db_connection.close_connection()

    # Delete book controller
    async def delete_book_controller(self, user_id: str, book_id: str) -> dict:
        """
        Delete book controller.
        """
        try:
            Config = Settings()
            mongo_db_connection = MongoDBConnection(Config.MONGO_URI, Config.DB_NAME)

            # Start the connection and get the book collection
            mongo_db_connection.start_connection()
            book_collection = mongo_db_connection.get_collection("books")
            delete_res = book_collection.delete_one({"user_id": user_id, "book_id": book_id})
            if delete_res.deleted_count:
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status":"success", "message":"Book deleted successfully."})
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to delete book! Book with this book_id doesn't exist." )
        except Exception as e:
            raise e
        finally:
            # Close the connection
            mongo_db_connection.close_connection()
        
