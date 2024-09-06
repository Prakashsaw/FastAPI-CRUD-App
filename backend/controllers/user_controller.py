from fastapi import APIRouter, HTTPException
from config.db import collection
from models.user_model import SignUpUser
from models.user_model import LoginUser
from schemas.user_schema import all_user_data, individual_user_data
import secrets
import string
from services.secure_password import encode_and_hash_password, verify_password

user_router = APIRouter()

async def get_all_user():
    try:
        all_users = collection.find()
        all_users_data = all_user_data(all_users)
        # print("All Users: ", all_users_data)
        return {"status_code": 200, "message": "All users fetched successfully!", "all_users": all_users_data}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error! Error: {str(e)}")
    

async def get_user_by_id(user_id: str):
    try:
        print("user_id: ", user_id)   
        
        user = collection.find_one({"user_id": user_id})
        print("User: ", user)

        if not user:
            return {"status_code": 404, "message": "User not found!"}
        
        return {"status_code": 200, "message": "User fetched successfully!", "user": individual_user_data(user)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error! Error: {str(e)}")
    

async def create_user(user: SignUpUser):
    try:
        user = dict(user)

        # Generate 10 digit alfanumeric unique nano id as a user primary key
        # Define the character set: uppercase letters, lowercase letters, and digits
        characters = string.ascii_letters + string.digits
        # Generate a secure random string of the specified length
        length = 20
        unique_id = ''.join(secrets.choice(characters) for _ in range(length))

        # Now add the unique_id to the user dict
        user["user_id"] = unique_id

        print("User: ", user)
        # First extract the password from the user dict
        password = user["password"]
        hashed_password = encode_and_hash_password(password)
        user["password"] = hashed_password
        
        # check that user dict has all required fields
        if user.get("name") is None or user.get("email") is None or user.get("password") is None:
            return {"status_code": 400, "message": "Any field can't be empty!"}
        
        # Check if user fields are empty or not, it should not be empty
        if user["name"] == "" or user["email"] == "" or user["password"] == "":
            return {"status_code": 400, "message": "All fields are required!"}
        
        # Check if user already exists
        if collection.find_one({"email": user["email"]}):
            return {"status_code": 400, "message": "User already exists!"}
        
        new_user = collection.insert_one(user)
        created_user = collection.find_one({"user_id": user["user_id"]})
       
        return {"status_code": 200, "message": "User created successfully!", "created_user": individual_user_data(created_user)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error! Error: {str(e)}")
    
async def login_user(user: LoginUser):
    try:
        user = dict(user)
        print("User: ", user)
        
        # First extract the password from the user dict
        email = user["email"]
        password = user["password"]

        if email == "" or password == "":
            return {"status_code": 400, "message": "All fields are required!"}
        
        user = collection.find_one({"email": email})
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
        
        return {"status_code": 200, "message": "User logged in successfully!", "user": individual_user_data(user)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error! Error: {str(e)}")
    
    
async def update_user(user_id: str, user: SignUpUser):
    try:
        user = dict(user)
        print("User: ", user)

        # Check if user fields are empty or not, it should not be empty
        if user["name"] == "" or user["email"] == "" or user["password"] == "":
            return {"status_code": 400, "message": "Any field can't be empty!"}
        
        collection.find_one_and_update({"user_id": user_id}, {"$set": user})

        updated_user = collection.find_one({"user_id": user_id})

        return {"status_code": 200, "message": "User updated successfully!", "updated_user": individual_user_data(updated_user)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error! Error: {str(e)}")
    
    
async def delete_user(user_id: str):
    try:
        user = collection.find_one({"user_id": user_id})
        if user is None:
            return {"status_code": 404, "message": "User not found!"}
        
        collection.find_one_and_delete({"user_id": user_id})

        return {"status_code": 200, "message": "User deleted successfully!"}
        
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error! Error: {str(e)}")
    
async def hello_world():
    return {"message": "Hello World!"}