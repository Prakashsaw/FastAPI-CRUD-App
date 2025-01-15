import bcrypt

SPECIAL_CHARACTERS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>']

def encode_and_hash_password(password: str) -> str:
    """Encode and hash the password using bcrypt"""
    # converting password to array of bytes 
    encoded_password = password.encode('utf-8') 

    # generating the salt 
    salt = bcrypt.gensalt() 

    # Hashing the password 
    hashed_password = bcrypt.hashpw(encoded_password, salt) 

    decoded_hashed_password = hashed_password.decode('utf-8') 

    return decoded_hashed_password

def verify_password(password: str, hashed_password: str) -> bool:
    """Check if the password matches with the hashed password"""
    # converting password to array of bytes 
    encoded_password = password.encode('utf-8') 

    encoded_hashed_password = hashed_password.encode('utf-8')

    # checking if the password matches with the hashed password 
    is_password_correct = bcrypt.checkpw(encoded_password, encoded_hashed_password)

    return is_password_correct

    
def is_password_strong_enough(password: str) -> bool:
    if len(password) < 8:
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not any(char in SPECIAL_CHARACTERS for char in password):
        return False

    return True

