from pydantic import BaseModel

class SignUpUser(BaseModel):
    name: str
    email: str
    password: str

class LoginUser(BaseModel):
    email: str
    password: str

class RefreshTokenStore(BaseModel):
    user_id: str
    email: str
    refresh_token: str

# User session schema
class UserSessionStore(BaseModel):
    session_id: str
    user_id: str
    email: str


class User(BaseModel):
    user_id: str
    name: str
    email: str
    password: str
    is_verified: bool
    created_at: str
    updated_at: str
    
# class UserVerificationToken(BaseModel):
#     user_id: str
#     token: str
#     email: str
