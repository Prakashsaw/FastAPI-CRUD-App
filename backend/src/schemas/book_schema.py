from pydantic import BaseModel


class AddBookRequest(BaseModel):
    """This module contains the schemas for the book model."""
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
    """This module contains the schemas for the book model."""
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
    """This module contains the schemas for the book model."""
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