import bcrypt

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

    