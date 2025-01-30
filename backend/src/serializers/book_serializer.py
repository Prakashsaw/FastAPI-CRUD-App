def book_data(data) -> dict:
    """
    Serialize book data.
    """
    return {
        "user_id": data["user_id"],
        "book_id": data["book_id"],
        "category": data["category"],
        "book_title": data["book_title"],
        "book_author": data["book_author"],
        "book_price": data["book_price"],
        "publisher": data["publisher"],
        "published_date": data["published_date"],
        "page_count": data["page_count"],
        "language": data["language"],
        "book_rating": data["book_rating"],
        "book_image": data["book_image"],
        "created_at": data["created_at"],
        "updated_at": data["updated_at"],
    }
    

def all_books_data(all_data) -> list:
    """
    Serialize all books data.
    """
    return [book_data(data) for data in all_data]