from fastapi import HTTPException
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.config.jwt_token import create_access_token, create_refresh_token, decode_jwt_token
from jwt import InvalidTokenError, ExpiredSignatureError

# Mock configurations
MOCK_ALGORITHM = "HS256"
MOCK_ACCESS_SECRET_KEY = "jwt_access_token_a1b2c3d4e5f6g7h8i9j0"
MOCK_REFRESH_SECRET_KEY = "jwt_refresh_token_a1b2c3d4e5f6g7h8i9j0"
MOCK_ACCESS_EXPIRY_MINUTES = 30
MOCK_REFRESH_EXPIRY_DAYS = 7

# Mock payload
MOCK_PAYLOAD = {"user_id": "QSGFEHJ4875YKFBKJHFK", 
                "email": "test@gmail.com", 
                "session_id": "1234"}

@pytest.fixture
def mock_config():
    """Mock Config settings."""
    with patch("src.config.jwt_token.Config") as MockConfig:
        MockConfig.JWT_ALGORITHM = MOCK_ALGORITHM
        MockConfig.JWT_ACCESS_SECRET_KEY = MOCK_ACCESS_SECRET_KEY
        MockConfig.JWT_REFRESH_SECRET_KEY = MOCK_REFRESH_SECRET_KEY
        MockConfig.JWT_ACCESS_EXPIRY_MINUTES = MOCK_ACCESS_EXPIRY_MINUTES
        MockConfig.JWT_REFRESH_EXPIRY_DAYS = MOCK_REFRESH_EXPIRY_DAYS
        yield MockConfig

@pytest.fixture
def mock_jwt():
    """Mock the jwt library."""
    with patch("src.config.jwt_token.jwt") as MockJwt:
        yield MockJwt

def test_create_access_token(mock_config, mock_jwt):
    """Test creating an access token."""
    mock_jwt.encode.return_value = "mock_access_token"

    token = create_access_token(MOCK_PAYLOAD)

    # Assert jwt.encode is called with correct arguments
    mock_jwt.encode.assert_called_once_with(
        {**MOCK_PAYLOAD, "exp": pytest.approx(datetime.now() + timedelta(minutes=MOCK_ACCESS_EXPIRY_MINUTES), abs=2)},
        MOCK_ACCESS_SECRET_KEY,
        algorithm=MOCK_ALGORITHM
    )
    assert token == "mock_access_token"

def test_create_refresh_token(mock_config, mock_jwt):
    """Test creating a refresh token."""
    mock_jwt.encode.return_value = "mock_refresh_token"

    token = create_refresh_token(MOCK_PAYLOAD)

    # Assert jwt.encode is called with correct arguments
    mock_jwt.encode.assert_called_once_with(
        {**MOCK_PAYLOAD, "exp": pytest.approx(datetime.now() + timedelta(days=MOCK_REFRESH_EXPIRY_DAYS), abs=2)},
        MOCK_REFRESH_SECRET_KEY,
        algorithm=MOCK_ALGORITHM
    )
    assert token == "mock_refresh_token"

def test_decode_jwt_token_valid(mock_config, mock_jwt):
    """Test decoding a valid token."""
    mock_jwt.decode.return_value = MOCK_PAYLOAD

    payload = decode_jwt_token("mock_token", is_refresh=False)

    mock_jwt.decode.assert_called_once_with(
        "mock_token", MOCK_ACCESS_SECRET_KEY, algorithms=[MOCK_ALGORITHM]
    )
    assert payload == MOCK_PAYLOAD

def test_decode_jwt_token_expired(mock_config, mock_jwt):
    """Test decoding an expired token."""
    # Simulate jwt.decode raising ExpiredSignatureError
    mock_jwt.decode.side_effect = ExpiredSignatureError

    # Expect an HTTPException to be raised
    with pytest.raises(HTTPException) as excinfo:
        decode_jwt_token("mock_token", is_refresh=False)

    # Verify the HTTPException details
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Token has expired!"

# def test_decode_jwt_token_invalid(mock_config, mock_jwt):
#     """Test decoding an invalid token."""
#     mock_jwt.decode.side_effect = jwt.InvalidTokenError

#     with pytest.raises(Exception) as excinfo:
#         decode_jwt_token("mock_token", is_refresh=False)

#     assert excinfo.value.status_code == 401
#     assert "Invalid token!" in str(excinfo.value)
