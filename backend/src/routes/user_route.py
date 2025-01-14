from fastapi import APIRouter

from src.controllers.user_controller import sign_up_user, login_user, get_all_user, get_user_by_id, delete_user

user_router = APIRouter()

user_router.post("/signup")(sign_up_user)
user_router.post("/login")(login_user)

user_router.get("/get-all-user")(get_all_user)
user_router.get("/get-user/{user_id}")(get_user_by_id)
# user_router.put("/update-user/{user_id}")(update_user)
user_router.delete("/delete-user/{user_id}")(delete_user)



