import jwt
from dotenv import load_dotenv
from datetime import datetime
from datetime import timedelta
import os
load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRY_DAY = int(os.getenv("JWT_EXPIRY_DAY")) 

def create_jwt_token(payload: dict):
    # manupulate paylod and add expiry time
    payload["exp"] = datetime.now() + timedelta(days=JWT_EXPIRY_DAY)
    try:
        # create jwt token
        jwt_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return jwt_token
    except Exception as e:
        return {"error": str(e)}

def decode_jwt_token(jwt_token: str):
    try:
        payload = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired!"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token!"}
    except Exception as e:
        return {"error": str(e)}