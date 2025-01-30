import secrets
import string


def generate_unique_key():
    """
    Generate 20 digit alfanumeric unique nano id as a user primary key
    Define the character set: uppercase letters, lowercase letters, and digits
    """
    characters = string.ascii_uppercase + string.digits
    length = 20
    unique_id = ''.join(secrets.choice(characters) for _ in range(length))

    return unique_id

# def unique_string(byte: int = 8) -> str:
#     return secrets.token_urlsafe(byte)
