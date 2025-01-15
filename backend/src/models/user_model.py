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

class User(BaseModel):
    user_id: str
    name: str
    email: str
    password: str
    is_verified: bool = False
    created_at: str
    updated_at: str

    # def get_context_string(self, context: str) -> str:
    #     return f"{self.user_id}{context}{self.created_at}"

class UserVerificationToken(BaseModel):
    user_id: str
    token: str
    email: str