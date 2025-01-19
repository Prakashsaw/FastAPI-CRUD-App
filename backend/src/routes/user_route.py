from fastapi import APIRouter, Depends

from src.schemas.user_schema import LoginUser, SignUpUser
from src.controllers.user_controller import UserControllersClass
from src.dependencies.user_auth_dependency import token_required
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# , get_all_user, get_user_by_id, update_user, delete_user
user_router = APIRouter()
security = HTTPBearer()
user_controllers = UserControllersClass()

# Public routes
@user_router.post("/signup")
async def sign_up(signup_user_payload: SignUpUser) -> dict:
    """
    Sign up route.
    """
    return await user_controllers.signup_user(signup_user_payload)

@user_router.post("/login")
async def log_in(login_user_payload: LoginUser) -> dict:
    """
    Log in route.
    """
    return await user_controllers.login_user(login_user_payload)

# Protected routes

# Refresh token route
@user_router.post("/refresh-token", dependencies=[Depends(token_required(is_refresh=True))])
async def refresh_token(decoded_token_payload: dict = Depends(token_required(is_refresh=True))) -> dict:
    """
    Refresh token route.
    """
    
    return await user_controllers.refresh_token_controller(decoded_token_payload)

# user logout route
@user_router.post("/logout", dependencies=[Depends(token_required(is_refresh=False))])
async def logout(decoded_token_payload: dict = Depends(token_required(is_refresh=False))) -> dict:
    """
    Logout user route.
    """
    return await user_controllers.logout_user(decoded_token_payload)





