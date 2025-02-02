from fastapi import HTTPException, status
from typing import List
from fastapi.responses import JSONResponse
from datetime import datetime

from src.config.database import MongoDBConnection
from src.utils.generate_unique_key import generate_unique_key
from src.serializers.book_serializer import book_data, all_books_data
from src.config.env_setting import Settings


class BookController:
    """
    Controller class for managing book-related operations.
    """

    def __init__(self):
        self.Config = Settings()
        self.mongo_db_connection = MongoDBConnection(self.Config.MONGO_URI, self.Config.DB_NAME)
        self.collection_name = "books"

    def _start_connection(self):
        """
        Helper method to start MongoDB connection.
        """
        self.mongo_db_connection.start_connection()

    def _get_collection(self, collection_name: str):
        """
        Helper method to get MongoDB collection.
        """
        # self.mongo_db_connection.start_connection()
        return self.mongo_db_connection.get_collection(collection_name)

    def _close_connection(self):
        """
        Helper method to close MongoDB connection.
        """
        self.mongo_db_connection.close_connection()

    async def add_book(self, data: dict, user_id: str) -> dict:
        """
        Add a new book for a user.
        """
        unique_id = generate_unique_key()
        timestamp = str(datetime.now())

        add_payload = {
            "user_id": user_id,
            "book_id": unique_id,
            "category": data.get("category"),
            "book_title": data.get("book_title"),
            "book_author": data.get("book_author"),
            "book_price": data.get("book_price"),
            "publisher": data.get("publisher"),
            "published_date": data.get("published_date"),
            "page_count": data.get("page_count"),
            "language": data.get("language"),
            "book_rating": data.get("book_rating"),
            "book_image": data.get("book_image"),
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        try:
            self._start_connection()

            book_collection = self._get_collection(self.collection_name)
            res = book_collection.insert_one(add_payload)
            if res.inserted_id:
                inserted_book = book_collection.find_one({"book_id": unique_id})
                if inserted_book:
                    serialized_book = book_data(inserted_book)
                    return JSONResponse(
                        status_code=status.HTTP_201_CREATED,
                        content={"status": "success", "message": "Book added successfully.", "book": serialized_book},
                    )
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get inserted book")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add book")
        except Exception as e:
            raise e
        finally:
            self._close_connection()

    async def get_all_books(self, user_id: str) -> List[dict]:
        """
        Fetch all books for a user.
        """
        try:
            self._start_connection()

            book_collection = self._get_collection(self.collection_name)
            all_books = book_collection.find({"user_id": user_id})
            if all_books:
                serialized_books = all_books_data(all_books)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={"status": "success", "message": "All the books fetched successfully.", "books": serialized_books},
                )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found")
        except Exception as e:
            raise e
        finally:
            self._close_connection()

    async def get_book_by_id(self, user_id: str, book_id: str) -> dict:
        """
        Fetch a specific book by ID for a user.
        """
        try:
            self._start_connection()

            book_collection = self._get_collection(self.collection_name)
            book = book_collection.find_one({"user_id": user_id, "book_id": book_id})
            if book:
                serialized_book = book_data(book)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={"status": "success", "message": "Book fetched successfully.", "book": serialized_book},
                )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        except Exception as e:
            raise e
        finally:
            self._close_connection()

    async def update_book(self, update_payload: dict, user_id: str, book_id: str) -> dict:
        """
        Update a book for a user.
        """
        try:
            self._start_connection()

            book_collection = self._get_collection(self.collection_name)
            update_payload["updated_at"] = str(datetime.now())
            update_res = book_collection.update_one(
                {"user_id": user_id, "book_id": book_id}, {"$set": update_payload}
            )
            if update_res.modified_count:
                updated_book = book_collection.find_one({"user_id": user_id, "book_id": book_id})
                if updated_book:
                    serialized_book = book_data(updated_book)
                    return JSONResponse(
                        status_code=status.HTTP_200_OK,
                        content={"status": "success", "message": "Book updated successfully.", "book": serialized_book},
                    )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found or no changes made")
        except Exception as e:
            raise e
        finally:
            self._close_connection()

    async def delete_book(self, user_id: str, book_id: str) -> dict:
        """
        Delete a book for a user.
        """
        try:
            self._start_connection()
            
            book_collection = self._get_collection(self.collection_name)
            delete_res = book_collection.delete_one({"user_id": user_id, "book_id": book_id})
            if delete_res.deleted_count:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={"status": "success", "message": "Book deleted successfully."},
                )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        except Exception as e:
            raise e
        finally:
            self._close_connection()
            