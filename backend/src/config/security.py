import bcrypt
from typing import Optional


class PasswordManager:
    """
    A class to handle password hashing, verification, and strength validation.
    """

    @staticmethod
    def encode_and_hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.

        :param password: The password to hash.
        :return: The hashed password as a string.
        :raises ValueError: If the password is empty or invalid.
        """
        if not password:
            raise ValueError("Password cannot be empty.")

        try:
            # Convert password to bytes
            encoded_password = password.encode('utf-8')

            # Generate salt and hash the password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(encoded_password, salt)

            # Return the hashed password as a string
            return hashed_password.decode('utf-8')
        except Exception as e:
            raise RuntimeError(f"Error encoding and hashing password: {str(e)}")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify if the provided password matches the hashed password.

        :param password: The password to verify.
        :param hashed_password: The hashed password to compare against.
        :return: True if the password matches the hashed password, False otherwise.
        :raises ValueError: If either password or hashed_password is empty or invalid.
        """
        if not password or not hashed_password:
            raise ValueError("Password and hashed password cannot be empty.")

        try:
            # Convert both password and hashed password to bytes
            encoded_password = password.encode('utf-8')
            encoded_hashed_password = hashed_password.encode('utf-8')

            # Verify if the password matches the hashed password
            return bcrypt.checkpw(encoded_password, encoded_hashed_password)
        except Exception as e:
            raise RuntimeError(f"Error verifying password: {str(e)}")

    @staticmethod
    def is_password_strong_enough(password: str) -> bool:
        """
        Check if the provided password meets the strength requirements.

        Password must contain at least:
        - 8 characters
        - One uppercase letter
        - One lowercase letter
        - One digit
        - One special character from a predefined set

        :param password: The password to check.
        :return: True if the password is strong enough, False otherwise.
        """
        SPECIAL_CHARACTERS = {'@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>'}

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