from fastapi import HTTPException
from jwt import InvalidTokenError, ExpiredSignatureError
import jwt
from datetime import datetime, timedelta
from src.config.env_setting import Settings


def create_access_token(payload: dict):
    Config = Settings()
    JWT_ALGORITHM = Config.JWT_ALGORITHM
    JWT_ACCESS_SECRET_KEY = Config.JWT_ACCESS_SECRET_KEY
    JWT_ACCESS_EXPIRY_MINUTES = Config.JWT_ACCESS_EXPIRY_MINUTES
    # manupulate paylod and add expiry time
    payload["exp"] = datetime.now() + timedelta(minutes=JWT_ACCESS_EXPIRY_MINUTES)
    try:
        # create jwt token
        jwt_access_token = jwt.encode(payload, JWT_ACCESS_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return jwt_access_token
    except Exception as e:
        raise e
    
def create_refresh_token(payload: dict):
    Config = Settings()
    JWT_ALGORITHM = Config.JWT_ALGORITHM
    JWT_REFRESH_SECRET_KEY = Config.JWT_REFRESH_SECRET_KEY
    JWT_REFRESH_EXPIRY_DAYS = Config.JWT_REFRESH_EXPIRY_DAYS
    # manupulate paylod and add expiry time
    payload["exp"] = datetime.now() + timedelta(days=JWT_REFRESH_EXPIRY_DAYS)
    try:
        # create jwt token
        jwt_refresh_token = jwt.encode(payload, JWT_REFRESH_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return jwt_refresh_token
    except Exception as e:
        raise e
    
def decode_jwt_token(token: str, is_refresh: bool):
    Config = Settings()
    JWT_ALGORITHM = Config.JWT_ALGORITHM
    JWT_ACCESS_SECRET_KEY = Config.JWT_ACCESS_SECRET_KEY
    JWT_REFRESH_SECRET_KEY = Config.JWT_REFRESH_SECRET_KEY
    secrete_key = JWT_REFRESH_SECRET_KEY if is_refresh else JWT_ACCESS_SECRET_KEY
    # print("secrete_key: ", secrete_key)
    # print("is_refresh: ", is_refresh)
    try:
        payload = jwt.decode(token, secrete_key, algorithms=[JWT_ALGORITHM])
        # print("Decoded Token user data: ", payload)
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired!")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token!")
    except Exception as e:
        raise e