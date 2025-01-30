from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError, InvalidTokenError

from src.config.jwt_token import JWTManager
from src.config.database import MongoDBConnection
from src.config.env_setting import Settings


security = HTTPBearer()


class TokenValidator:
    def __init__(self, is_refresh: bool):
        """
        Initializes the TokenValidator with the `is_refresh` flag.
        `is_refresh` determines whether the token is an access or refresh token.
        """
        self.is_refresh = is_refresh
        self.Config = Settings()
        self.mongo_db_connection = MongoDBConnection(self.Config.MONGO_URI, self.Config.DB_NAME)
        self.jwt_manager = JWTManager()

    async def _validate_token(self, credentials: HTTPAuthorizationCredentials):
        """
        Validates the token extracted from the Authorization header.
        Checks if the token is expired, invalid, or if the session is no longer valid.
        """
        if credentials is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
        
        token = credentials.credentials
        try:
            # Start the database connection
            self.mongo_db_connection.start_connection()

            # Decode the token and extract the data
            data = self.jwt_manager.decode_token(token, self.is_refresh)
            if data.get("error"):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=data["error"])

            # Check if the session_id exists in the database (user_sessions collection)
            session_id = data.get("session_id")
            user_session_collection = self.mongo_db_connection.get_collection("user_sessions")
            user_session = user_session_collection.find_one({"session_id": session_id})
            if not user_session:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                    "device_logged_out": True,
                    "message": "Invalid token. User session does not exist."
                })
            return data
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except Exception as e:
            raise e
        finally:
            # Ensure the database connection is closed after the operation
            self.mongo_db_connection.close_connection()

    async def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        """
        Makes the TokenValidator callable as a dependency, ensuring that token validation is performed
        for each request that requires it.
        """
        return await self._validate_token(credentials)

# Usage in FastAPI route
def token_required(is_refresh: bool):
    """
    Factory function to create token validation dependencies with a specified refresh flag.
    """
    validator = TokenValidator(is_refresh)
    return validator
