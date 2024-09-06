from fastapi import APIRouter

from controllers.user_controller import get_all_user, get_user_by_id, create_user, login_user, update_user, delete_user, hello_world

user_router = APIRouter()

user_router.get("/api/v1/user/get-all-user")(get_all_user)
user_router.get("/api/v1/user/get-user/{user_id}")(get_user_by_id)
user_router.post("/api/v1/user/create-user")(create_user)
user_router.post("/api/v1/user/login")(login_user)
user_router.put("/api/v1/user/update-user/{user_id}")(update_user)
user_router.delete("/api/v1/user/delete-user/{user_id}")(delete_user)

user_router.post("/api/v1/user/hello-world")(hello_world)

