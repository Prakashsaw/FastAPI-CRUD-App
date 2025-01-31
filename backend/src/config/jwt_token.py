from fastapi import HTTPException
import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone

from src.config.env_setting import Settings


class JWTManager:
    """
    A class to handle JWT creation and decoding for access and refresh tokens.
    """

    def __init__(self):
        self.config = Settings()
        self.algorithm = self.config.JWT_ALGORITHM
        self.access_secret = self.config.JWT_ACCESS_SECRET_KEY
        self.access_expiry_minutes = self.config.JWT_ACCESS_EXPIRY_MINUTES
        self.refresh_secret = self.config.JWT_REFRESH_SECRET_KEY
        self.refresh_expiry_days = self.config.JWT_REFRESH_EXPIRY_DAYS

    def create_access_token(self, payload: dict) -> str:
        """
        Create an access token with an expiry time.

        :param payload: The payload to encode in the token.
        :return: The generated JWT access token.
        """
        payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=self.access_expiry_minutes)
        try:
            return jwt.encode(payload, self.access_secret, algorithm=self.algorithm)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create access token: {str(e)}")

    def create_refresh_token(self, payload: dict) -> str:
        """
        Create a refresh token with an expiry time.

        :param payload: The payload to encode in the token.
        :return: The generated JWT refresh token.
        """
        payload["exp"] = datetime.now(timezone.utc) + timedelta(days=self.refresh_expiry_days)
        try:
            return jwt.encode(payload, self.refresh_secret, algorithm=self.algorithm)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create refresh token: {str(e)}")

    def decode_token(self, token: str, is_refresh: bool) -> dict:
        """
        Decode a JWT token and return the payload.

        :param token: The JWT token to decode.
        :param is_refresh: Whether the token is a refresh token.
        :return: The decoded payload.
        """
        secret_key = self.refresh_secret if is_refresh else self.access_secret
        try:
            payload = jwt.decode(token, secret_key, algorithms=[self.algorithm])
            return payload
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired!")
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token!")
        except Exception as e:
            raise e
        
    def decode_jwt_token_without_expirytime(self, token: str):
        """
        Decode the JWT token to extract the payload without validating expiration, but validate the signature.
        """
        try:
            # Decode with signature verification but without validating expiration time
            payload = jwt.decode(
                token,
                key=self.access_secret,
                algorithms=[self.algorithm],
                options={"verify_exp": False} 
            )
            return payload
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token!")
        except Exception as e:
            raise e
