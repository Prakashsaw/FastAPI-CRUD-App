from fastapi import APIRouter, Depends

from src.dependencies.user_auth_dependency import token_required
from src.schemas.book_schema import AddBookRequest, UpdateBookRequest 
from src.controllers.book_controller import BookController


book_router = APIRouter()
book_controllers = BookController()


@book_router.post("/add-book", dependencies=[Depends(token_required(is_refresh=False))])
async def add_book(add_book_payload: AddBookRequest, decoded_token_payload: dict = Depends(token_required(is_refresh=False))):
    """
    Add book route.
    """
    # print("add_book_payload: ", type(add_book_payload), type(dict(add_book_payload)))
    user_id = decoded_token_payload.get("user_id")
    added_book_res = await book_controllers.add_book(dict(add_book_payload), user_id)
    return added_book_res

@book_router.get("/all-books", dependencies=[Depends(token_required(is_refresh=False))])
async def get_all_books(decoded_token_payload: dict = Depends(token_required(is_refresh=False))):
    """
    Get all books route.
    """
    user_id = decoded_token_payload.get("user_id")
    all_books_res = await book_controllers.get_all_books(user_id)
    return all_books_res

@book_router.get("/one-book/{book_id}", dependencies=[Depends(token_required(is_refresh=False))])
async def get_book_by_id(book_id: str, decoded_token_payload: dict = Depends(token_required(is_refresh=False))):
    """
    Get book by ID route.
    """
    print("book_id: ", book_id)
    user_id = decoded_token_payload.get("user_id")
    one_book_res = await book_controllers.get_book_by_id(user_id, book_id)
    return one_book_res

@book_router.put("/update-book/{book_id}", dependencies=[Depends(token_required(is_refresh=False))])
async def update_book(book_id: str, update_book_payload: UpdateBookRequest, decoded_token_payload: dict = Depends(token_required(is_refresh=False))):
    """
    Update book route.
    """
    user_id = decoded_token_payload.get("user_id")
    updated_book_res = await book_controllers.update_book(dict(update_book_payload), user_id, book_id)
    return updated_book_res

@book_router.delete("/delete-book/{book_id}", dependencies=[Depends(token_required(is_refresh=False))])
async def delete_book(book_id: str, decoded_token_payload: dict = Depends(token_required(is_refresh=False))):
    """
    Delete book route.
    """
    user_id = decoded_token_payload.get("user_id")
    deleted_book_res = await book_controllers.delete_book(user_id, book_id)
    return deleted_book_res