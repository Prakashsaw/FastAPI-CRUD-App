from fastapi import APIRouter, HTTPException
from src.config.db import mongo_db_connection
from src.models.user_model import SignUpUser, LoginUser
from src.schemas.user_schema import all_user_data, individual_user_data
from src.utils.generate_unique_key import generate_unique_key
from src.utils.secure_password import encode_and_hash_password, verify_password
from src.utils.jwt_token import create_jwt_token, decode_jwt_token

user_router = APIRouter()

async def sign_up_user(user: SignUpUser):
    try:
        # Start the connection
        mongo_db_connection.start_connection()
        
        user = dict(user)
        
        # check that user dict has all required fields
        if user.get("name") is None or user.get("email") is None or user.get("password") is None:
            return {"status_code": 400, "message": "Any field can't be empty!"}
        
        # Check if user fields are empty or not, it should not be empty
        if user["name"] == "" or user["email"] == "" or user["password"] == "":
            return {"status_code": 400, "message": "All fields are required!"}
        
        # Get the user collection
        user_collection = mongo_db_connection.get_collection("users")

        # Check if user already exists
        if user_collection.find_one({"email": user["email"]}):
            return {"status_code": 400, "message": "User already exists!"}

        # Generate unique id for the user
        unique_id = generate_unique_key()
        # Now add the unique_id to the user dict
        user["user_id"] = unique_id

        print("User: ", user)
        # First extract the password from the user dict
        password = user["password"]
        hashed_password = encode_and_hash_password(password)
        user["password"] = hashed_password

        new_user = user_collection.insert_one(user)
        created_user = user_collection.find_one({"user_id": user["user_id"]})

        return {"status_code": 200, "message": "User created successfully!", "created_user": individual_user_data(created_user)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error! Error: {str(e)}")
    
    finally:
        # Close the connection
        mongo_db_connection.close_connection()
    
async def login_user(user: LoginUser):
    try:
        # Start the connection
        mongo_db_connection.start_connection()

        user = dict(user)
        print("User: ", user)
        
        # First extract the password from the user dict
        email = user["email"]
        password = user["password"]

        if email == "" or password == "":
            return {"status_code": 400, "message": "All fields are required!"}
        
        # Get the user collection
        user_collection = mongo_db_connection.get_collection("users")

        user = user_collection.find_one({"email": email})
        print("User: ", user)
        
        if user is None:
            return {"status_code": 404, "message": "User does not exist!"}
        
        # verify the password
        user_hashed_password = user["password"]
        print("User Hashed Password: ", type(user_hashed_password), user_hashed_password)
        is_password_correct = verify_password(password, user_hashed_password)
        print("Is Password Correct: ", is_password_correct)

        if is_password_correct == False:
            return {"status_code": 400, "message": "Password is incorrect!"}
        
        # Generate JWT token
        payload = {"user_id": user["user_id"], "email": user["email"]}
        jwt_token = create_jwt_token(payload)

        return {"status_code": 200, "message": "User logged in successfully!", "user": individual_user_data(user), "jwt_access_token": jwt_token}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error! Error: {str(e)}")
    
    finally:
        # Close the connection
        mongo_db_connection.close_connection()
    

async def get_all_user():
    try:
        # Start the connection
        mongo_db_connection.start_connection() 

        # Get the user collection
        user_collection = mongo_db_connection.get_collection("users")

        all_users = user_collection.find()
        all_users_data = all_user_data(all_users)

        # print("All Users: ", all_users_data)
        return {"status_code": 200, "message": "All users fetched successfully!", "all_users": all_users_data}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error! Error: {str(e)}")
    
    finally:
        # Close the connection
        mongo_db_connection.close_connection()
    

async def get_user_by_id(user_id: str):
    try:
        # Start the connection
        mongo_db_connection.start_connection()

        print("user_id: ", user_id) 

        # Get the user collection
        user_collection = mongo_db_connection.get_collection("users")

        user = user_collection.find_one({"user_id": user_id})
        print("User: ", user)

        if not user:
            return {"status_code": 404, "message": "User not found!"}

        return {"status_code": 200, "message": "User fetched successfully!", "user": individual_user_data(user)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error! Error: {str(e)}")
    
    finally:
        # Close the connection
        mongo_db_connection.close_connection()
    
    
# async def update_user(user_id: str, user: SignUpUser):
#     try:
#         # Start the connection
#         mongo_db_connection.start_connection()
#         # Get the user collection
#         user_collection = mongo_db_connection.get_collection("users")

#         # Before updating the user, first check if user is valid or not with jwt token which is passed in the header

#         user = dict(user)
#         print("User: ", user)

#         # Check if user fields are empty or not, it should not be empty
#         if user["name"] == "" or user["email"] == "" or user["password"] == "":
#             return {"status_code": 400, "message": " All fields are requiredS!"}
        
#         user = user_collection.find_one({"user_id": user_id})
        
#         if user is None:
#             return {"status_code": 404, "message": "User not found!"}
        
#         res = user_collection.find_one_and_update({"user_id": user_id}, {"$set": user})
#         # print("Res: ", res)

#         updated_user = user_collection.find_one({"user_id": user_id})
#         print("Updated User: ", updated_user)

#         return {"status_code": 200, "message": "User updated successfully!", "updated_user": individual_user_data(updated_user)}
#     except Exception as e:
#         return HTTPException(status_code=500, detail=f"Internal Server Error! Error: {str(e)}")
    
#     finally:
#         pass
#         # Close the connection
#         mongo_db_connection.close_connection()
    
    
async def delete_user(user_id: str):
    try:
        # Start the connection
        mongo_db_connection.start_connection()

        # Get the user collection
        user_collection = mongo_db_connection.get_collection("users")

        # Before deleting the user, first check if user is valid or not with jwt token which is passed in the header
        user = user_collection.find_one({"user_id": user_id})
        if user is None:
            return {"status_code": 404, "message": "User not found!"}
        
        user_collection.find_one_and_delete({"user_id": user_id})

        return {"status_code": 200, "message": "User deleted successfully!"}
        
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error! Error: {str(e)}")
    
    finally:
        # Close the connection
        mongo_db_connection.close_connection()
    
