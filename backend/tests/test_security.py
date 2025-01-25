import pytest
from src.config.security import (
    encode_and_hash_password,
    verify_password,
    is_password_strong_enough,
)
import bcrypt

# Test encode_and_hash_password
def test_encode_and_hash_password():
    password = "StrongP@ssw0rd"
    hashed_password = encode_and_hash_password(password)

    # Ensure the hashed password is not None or empty
    assert hashed_password is not None
    assert len(hashed_password) > 0

    # Ensure the hashed password is different from the original password
    assert hashed_password != password

    # Ensure the hashed password can be verified
    assert bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

# Test verify_password
def test_verify_password():
    password = "StrongP@ssw0rd"
    hashed_password = encode_and_hash_password(password)

    # Ensure correct password matches the hashed password
    assert verify_password(password, hashed_password) is True

    # Ensure incorrect password does not match the hashed password
    assert verify_password("WrongPassword", hashed_password) is False

# Test is_password_strong_enough
def test_is_password_strong_enough():
    # Test strong password
    assert is_password_strong_enough("StrongP@ssw0rd") is True

    # Test password too short
    assert is_password_strong_enough("S@1") is False

    # Test password missing uppercase letter
    assert is_password_strong_enough("weakp@ssw0rd") is False

    # Test password missing lowercase letter
    assert is_password_strong_enough("WEAKP@SSW0RD") is False

    # Test password missing digit
    assert is_password_strong_enough("WeakPassword!") is False

    # Test password missing special character
    assert is_password_strong_enough("WeakPassword1") is False
