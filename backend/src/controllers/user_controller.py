from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, status
import re
from src.config.database import mongo_db_connection
from src.models.user_model import SignUpUser, LoginUser
from src.schemas.user_schema import all_user_data, individual_user_data
from src.config.security import encode_and_hash_password, verify_password, is_password_strong_enough
from src.utils.generate_unique_key import generate_unique_key
from src.config.jwt_token import create_jwt_token, decode_jwt_token
from src.controllers.send_email_controller import send_account_verification_email
from src.config.env_setting import Config

user_router = APIRouter()

async def sign_up_user(user: SignUpUser):
    try:
        # Start the connection
        mongo_db_connection.start_connection()
        
        user = dict(user)
        
        # check that user dict has all required fields
        if user.get("name") is None or user.get("email") is None or user.get("password") is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields are required!")
        
        # Check if user fields are empty or not, it should not be empty
        if user["name"] == "" or user["email"] == "" or user["password"] == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields are required!")
        
        # check that email format is correct or not
        email_string_match = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        if not re.match(email_string_match, user["email"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is not valid!")
        
        # Password should be strong enough
        if not is_password_strong_enough(user["password"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a strong password.")
        
        # Get the user collection
        user_collection = mongo_db_connection.get_collection("users")

        # Check if user already exists
        if user_collection.find_one({"email": user["email"]}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists!")

        # Generate unique id for the user
        unique_id = generate_unique_key()
        # Now add the unique_id to the user dict
        user["user_id"] = unique_id
        user["is_verified"] = False

        print("User: ", user)
        # First extract the password from the user dict
        password = user["password"]
        hashed_password = encode_and_hash_password(password)
        user["password"] = hashed_password

        # Generate JWT token for making email verification link
        payload = {"user_id": user["user_id"], "email": user["email"]}
        token = create_jwt_token(payload)
        print("Token: ", token)
        user_email = user["email"]
        activate_url = f"{Config.FRONTEND_HOST}/auth/account-verify?token={token}&email={user_email}"
        res1 = await send_account_verification_email(user, background_tasks=BackgroundTasks(), activate_url=activate_url)
        print("Res1: ", res1)

        new_user = user_collection.insert_one(user)
        created_user = user_collection.find_one({"user_id": user["user_id"]})

        return {"status_code": status.HTTP_201_CREATED, "message": "User created successfully. Email verification link has been sent to your email, please verify your email!", "created_user": individual_user_data(created_user)}
        
        # return {"status_code": status.HTTP_201_CREATED, "message": "User created successfully!", "created_user": individual_user_data(created_user)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}")
    
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
            # return {"status_code": 400, "message": "All fields are required!"}
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields are required!")
        
        # Get the user collection
        user_collection = mongo_db_connection.get_collection("users")

        user = user_collection.find_one({"email": email})
        print("User: ", user)
        
        if user is None:
            # return {"status_code": 404, "message": "User does not exist!"}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist!")
        
        # verify the password
        user_hashed_password = user["password"]
        print("User Hashed Password: ", type(user_hashed_password), user_hashed_password)
        is_password_correct = verify_password(password, user_hashed_password)
        print("Is Password Correct: ", is_password_correct)

        if is_password_correct == False:
            # return {"status_code": 400, "message": "Password is incorrect!"}
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect!")
        
        # Generate JWT token
        payload = {"user_id": user["user_id"], "email": user["email"]}
        jwt_token = create_jwt_token(payload)

        return {"status_code": status.HTTP_200_OK, "message": "User logged in successfully!", "user": individual_user_data(user), "jwt_access_token": jwt_token}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}")
    
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
        return HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
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
            # return {"status_code": 404, "message": "User not found!"}
            raise HTTPException(status_code=404, detail="User not found!")

        return {"status_code": 200, "message": "User fetched successfully!", "user": individual_user_data(user)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    finally:
        # Close the connection
        mongo_db_connection.close_connection()
    
    
async def update_user(user_id: str, user: SignUpUser):
    try:
        # Start the connection
        mongo_db_connection.start_connection()
        # Get the user collection
        user_collection = mongo_db_connection.get_collection("users")

        # Before updating the user, first check if user is valid or not with jwt token which is passed in the header

        user = dict(user)
        print("User: ", user)

        # Check if user fields are empty or not, it should not be empty
        if user["name"] == "" or user["email"] == "" or user["password"] == "":
            # return {"status_code": 400, "message": " All fields are requiredS!"}
            raise HTTPException(status_code=400, detail="All fields are required!")
        
        user = user_collection.find_one({"user_id": user_id})
        
        if user is None:
            # return {"status_code": 404, "message": "User not found!"}
            raise HTTPException(status_code=404, detail="User not found!")
        
        res = user_collection.find_one_and_update({"user_id": user_id}, {"$set": user})
        # print("Res: ", res)

        updated_user = user_collection.find_one({"user_id": user_id})
        print("Updated User: ", updated_user)

        return {"status_code": 200, "message": "User updated successfully!", "updated_user": individual_user_data(updated_user)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    finally:
        pass
        # Close the connection
        mongo_db_connection.close_connection()
    
    
async def delete_user(user_id: str):
    try:
        # Start the connection
        mongo_db_connection.start_connection()

        # Get the user collection
        user_collection = mongo_db_connection.get_collection("users")

        # Before deleting the user, first check if user is valid or not with jwt token which is passed in the header
        user = user_collection.find_one({"user_id": user_id})
        if user is None:
            # return {"status_code": 404, "message": "User not found!"}
            raise HTTPException(status_code=404, detail="User not found!")
        
        user_collection.find_one_and_delete({"user_id": user_id})

        return {"status_code": 200, "message": "User deleted successfully!"}
        
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error! Error: {str(e)}")
    
    finally:
        # Close the connection
        mongo_db_connection.close_connection()
    
