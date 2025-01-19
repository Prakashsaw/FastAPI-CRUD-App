# Shcemas for books model
from pydantic import BaseModel

class AddBookRequest(BaseModel): # this is the schema for adding a book and this will remain same for the update book request
    category: str
    book_title: str
    book_author: str
    book_price: float
    publisher: str
    published_date: str
    page_count: int
    language: str
    book_rating: float
    book_image: str
    

class Book(BaseModel):
    user_id: str # for the reference of the user who added the book
    book_id: str
    category: str
    book_title: str
    book_author: str
    book_price: float
    publisher: str
    published_date: str
    page_count: int
    language: str
    book_rating: float
    book_image: str
    created_at: str
    updated_at: str

class UpdateBookRequest(BaseModel):
    category: str
    book_title: str
    book_author: str
    book_price: float
    publisher: str
    published_date: str
    page_count: int
    language: str
    book_rating: float
    book_image: str