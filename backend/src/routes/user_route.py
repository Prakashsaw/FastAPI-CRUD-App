from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.schemas.user_schema import LoginUser, SignUpUser
from src.controllers.user_controller import UserControllersClass
from src.dependencies.user_auth_dependency import token_required


user_router = APIRouter()
security = HTTPBearer()
user_controllers = UserControllersClass()


# Public routes
@user_router.post("/signup")
async def sign_up(signup_user_payload: SignUpUser, background_tasks: BackgroundTasks):
    """
    Sign up route.
    """
    return await user_controllers.signup_user(dict(signup_user_payload), background_tasks)

@user_router.post("/login")
async def log_in(login_user_payload: LoginUser, background_tasks: BackgroundTasks):
    """
    Log in route.
    """
    return await user_controllers.login_user(dict(login_user_payload), background_tasks)

@user_router.post("/user-account-verification/{token}/{email}")
async def user_account_verification(token:str, email: str, background_tasks: BackgroundTasks):
    """
    user account verification route.
    """
    return await user_controllers.user_account_verification_controller(token, background_tasks)


# Protected routes
@user_router.post("/refresh-token", dependencies=[Depends(token_required(is_refresh=True))])
async def refresh_token(decoded_token_payload: dict = Depends(token_required(is_refresh=True))):
    """
    Refresh token route.
    """
    
    return await user_controllers.refresh_token_controller(decoded_token_payload)

@user_router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Logout user route.
    """
    # Ensure credentials are provided
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Token is missing")
    
    token = credentials.credentials  # Extract the token from the header
    return await user_controllers.logout_user(token)


