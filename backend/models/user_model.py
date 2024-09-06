from pydantic import BaseModel
from datetime import datetime

class SignUpUser(BaseModel):
    name: str
    email: str
    password: str
    created_at: str = str(datetime.now())
    updated_at: str = str(datetime.now())

class LoginUser(BaseModel):
    email: str
    password: str