from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.config.jwt_token import decode_jwt_token
from jwt import ExpiredSignatureError, InvalidTokenError
from src.config.database import mongo_db_connection

# HTTPBearer for extracting token from Authorization header
security = HTTPBearer()

def token_required(is_refresh: bool):
    """
    Dependency factory for token validation.
    Allows passing `is_refresh` to differentiate between access and refresh tokens.
    """
    # Dependency for token validation
    async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        # print("credentials: ", credentials)
        if credentials is None:
            raise HTTPException(status_code=401, detail="Token is missing")
        
        token = credentials.credentials  # Extract the token from the header
        # print("token: ", token)
        try:
            # Decode the token
            # print("is_refresh: ", is_refresh)
            data = decode_jwt_token(token, is_refresh)
            # print("data: ", data)
            if data.get("error"):
                raise HTTPException(status_code=401, detail=data["error"])
            
            # Extract session_id from the decoded token payload and first check if it exists in the database (session collection) or not
            # We need to check this because the user might have logged out or logged In in another devide and the session_id might have been deleted from the database
            # If the session_id (means user session) does not exist in the database, then we need to invalidate the token
            session_id = data.get("session_id")
            mongo_db_connection.start_connection()
            user_session_collection = mongo_db_connection.get_collection("user_sessions")
            user_session = user_session_collection.find_one({"session_id": session_id})
            if not user_session:
                raise HTTPException(status_code=401, detail="Invalid token. User session does not exist.")

            # Return the decoded token data (e.g., user information)
            return data
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        finally:
            # Close the connection
            mongo_db_connection.close_connection()
        
    return validate_token
