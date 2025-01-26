from fastapi import HTTPException, status, BackgroundTasks
import re
from datetime import datetime
from src.config.database import MongoDBConnection
from src.serializers.user_serializer import individual_user_data
from src.config.security import encode_and_hash_password, verify_password, is_password_strong_enough
from src.utils.generate_unique_key import generate_unique_key
from src.config.jwt_token import create_access_token, create_refresh_token
from fastapi.responses import JSONResponse
from src.config.env_setting import Settings
from src.services.email_services import EmailServices
from src.config.jwt_token import decode_jwt_token
from src.config.email_config import test_fastmail

class UserControllersClass:
    async def signup_user(self, user: dict, background_tasks: BackgroundTasks):
        try:
            Config = Settings()
            mongo_db_connection = MongoDBConnection(Config.MONGO_URI, Config.DB_NAME)

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
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is not valid! Email format should be: test@example.com, email@domain.com, ect...")
            
            # Password should be strong enough
            if not is_password_strong_enough(user["password"]):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a strong password. Password should be at least 8 characters long and should contain at least one uppercase letter, one lowercase letter, one number and one special character. Example: Test@123, StrongPassword!123")
            
            # Get the user collection
            user_collection = mongo_db_connection.get_collection("users")

            # Check if user already exists
            if user_collection.find_one({"email": user["email"]}):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists!")

            # Generate unique id for the user
            unique_id = generate_unique_key()
            created_at = str(datetime.now())
            updated_at = str(datetime.now())

            # First extract the password from the user dict
            password = user["password"]
            hashed_password = encode_and_hash_password(password)

            # print("User: ", user)
            # Now make the payload for the user
            user_payload = {"user_id": unique_id,
                            "name": user["name"],
                            "email": user["email"],
                            "password": hashed_password,
                            "is_verified": False,
                            "created_at": created_at,
                            "updated_at": updated_at 
                            }
            
            # Before inserting the user into database first send the email verification link to the user email and if email sent successfully then insert the user into the database
            # Generate JWT token for making email verification link
            payload = {"user_id": user_payload["user_id"], "email": user_payload["email"]}
            email_verification_token = create_access_token(payload)
            user_email = user_payload["email"]
            activate_url = f"{Config.FRONTEND_HOST}/user-auth/account-verify?token={email_verification_token}&email={user_email}"

            # Send account verification email
            email_services = EmailServices()
            res1 = await email_services.send_account_verification_email(user_payload, background_tasks=background_tasks, activate_url=activate_url)
            if res1 is not True:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User not created! Failed to send account verification email!")

            new_user = user_collection.insert_one(user_payload)
            if new_user.inserted_id is None:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User not created! Please try again.")
            
            created_user = user_collection.find_one({"user_id": user_payload["user_id"]})

            # Json response
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={"status":"success", "message":"User created successfully. Please check your email box and verify your account.", "user":individual_user_data(created_user)})
            
        except Exception as e:
            raise e
        
        finally:
            # Close the connection
            mongo_db_connection.close_connection()
        
    async def login_user(self, user: dict, background_tasks: BackgroundTasks):
        try:
            Config = Settings()
            mongo_db_connection = MongoDBConnection(Config.MONGO_URI, Config.DB_NAME)

            # Start the connection
            mongo_db_connection.start_connection()

            user = dict(user)
            # print("User: ", user)
            
            email = user.get("email", "")
            password = user.get("password", "")
            if not email or not password:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields are required!")

            user_collection = mongo_db_connection.get_collection("users")
            fetched_user = user_collection.find_one({"email": email})

            if not fetched_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist!")

            fetched_user = dict(fetched_user)

            if not verify_password(password, fetched_user["password"]):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect!")

            if not fetched_user.get("is_verified"):
                payload = {"user_id": fetched_user["user_id"], "email": fetched_user["email"]}
                email_verification_token = create_access_token(payload)
                activate_url = f"{Config.FRONTEND_HOST}/user-auth/account-verify?token={email_verification_token}&email={email}"

                email_services = EmailServices()
                res1 = await email_services.send_account_verification_email(user=fetched_user, background_tasks=background_tasks, activate_url=activate_url)
                # print("Email send result:", res1)

                if not res1:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send account verification email!")

                # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not verified! Please check your email.")
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status":"failed", "message":"User is not verified! Please check your email."})
            
            # delete or revoke user's previous session if exists: This is done to prevent multiple logins from different devices
            # Get the user session collection
            user_session_collection = mongo_db_connection.get_collection("user_sessions")
            user_session_collection.delete_many({"user_id": fetched_user["user_id"], "email": fetched_user["email"]})

            # Create session for the user
            session_id = generate_unique_key()

            # Create JWT Access token and JWT Refresh token
            # session_id is also added to the payload to identify the user session during the access token and refresh token verification while calling to any protected route
            jwt_payload = { "user_id": fetched_user["user_id"],
                            "email": fetched_user["email"],
                            "session_id": session_id }
            
            jwt_access_token = create_access_token(jwt_payload)
            jwt_refresh_token = create_refresh_token(jwt_payload)

            # Create the user session information and store it in the database
            user_session_payload = {"session_id": session_id,
                                    "user_id": fetched_user["user_id"],
                                    "email": fetched_user["email"] }

            user_session_collection.insert_one(user_session_payload)

            # Delete or revoke user's previous refresh token if exists
            refresh_token_collection = mongo_db_connection.get_collection("refresh_tokens")
            refresh_token_collection.delete_many({"user_id": fetched_user["user_id"], "email": fetched_user["email"]})

            # Store the refresh token in the database
            refresh_token_collection.insert_one({"user_id": fetched_user["user_id"], "email": fetched_user["email"], "refresh_token": jwt_refresh_token})

            return JSONResponse(status_code=status.HTTP_200_OK, content={"status":"success", "message":"User logged in successfully!", "user":individual_user_data(fetched_user), "jwt_access_token": jwt_access_token, "jwt_refresh_token": jwt_refresh_token, "session_id": session_id})
        
        except Exception as e:
            raise e
        
        finally:
            # Close the connection
            mongo_db_connection.close_connection()
        
    async def user_account_verification_controller(self, token:str, background_tasks: BackgroundTasks):
        try:
            Config = Settings()
            mongo_db_connection = MongoDBConnection(Config.MONGO_URI, Config.DB_NAME)

            # Start the connection
            mongo_db_connection.start_connection()

            # Validate and then decode token that user has try to verify email by clickimg that link in valid time (within 30 minutes)
            decoded_data_dict = decode_jwt_token(token, is_refresh = False)
            # print("data: ", data)
            if decoded_data_dict.get("error"):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=decoded_data_dict["error"])
            
            user_id = decoded_data_dict["user_id"]
            email = decoded_data_dict["email"]

            # Get the user collection
            user_collection = mongo_db_connection.get_collection("users")

            user = user_collection.find_one({"user_id": user_id, "email": email})
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
            
            # Update the user is_verified field to True
            user_collection.find_one_and_update({"user_id": user_id, "email": email}, {"$set": {"is_verified": True}})

            # Send account activation confirmation email
            email_services = EmailServices()
            res = await email_services.send_account_verification_confirmation_email(user, background_tasks)
            if res is not True:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send account activation confirmation email!")

            return JSONResponse(status_code=status.HTTP_200_OK, content={"status":"success", "message":"User account verified successfully. Login to continue."})
        
        except Exception as e:
            raise e
        
        finally:
            # Close the connection
            mongo_db_connection.close_connection()

    async def refresh_token_controller(self, decoded_token_payload: dict):
        try:
            Config = Settings()
            mongo_db_connection = MongoDBConnection(Config.MONGO_URI, Config.DB_NAME)

            # Start the connection
            mongo_db_connection.start_connection()
            
            user_id = decoded_token_payload["user_id"]
            email = decoded_token_payload["email"]
            session_id = decoded_token_payload["session_id"]

            # First check if the user session exists or not: This is done to prevent the user from accessing the refresh token route if the user session is not valid means 
            # user is not logged in in multiple devices at the same time
            user_session_collection = mongo_db_connection.get_collection("user_sessions")
            user_session = user_session_collection.find_one({"user_id": user_id, "session_id": session_id})
            if user_session is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User session is not valid! Please login again to continue.")

            # Get the refresh token collection
            refresh_tokens_collection = mongo_db_connection.get_collection("refresh_tokens")
            refresh_token_store = refresh_tokens_collection.find_one({"user_id": user_id, "email": email})
            if refresh_token_store is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token!")
            
            # Generate new access token and refresh token and send it back to the user
            jwt_payload = {"user_id": user_id,
                        "email": email,
                        "session_id": session_id }
            jwt_access_token = create_access_token(jwt_payload)

            # Fetch the refresh token from the database
            jwt_refresh_token = refresh_token_store["refresh_token"]

            return JSONResponse(status_code=status.HTTP_200_OK, content={"status":"success", "message":"Access token refreshed successfully!", "jwt_access_token": jwt_access_token, "jwt_refresh_token": jwt_refresh_token, "session_id": session_id})
        
        except Exception as e:
            raise e
        
        finally:
            # Close the connection
            mongo_db_connection.close_connection()

    # User logout controller
    async def logout_user(self, decoded_token_payload: dict):
        try:
            Config = Settings()
            mongo_db_connection = MongoDBConnection(Config.MONGO_URI, Config.DB_NAME)

            # Start the connection
            mongo_db_connection.start_connection()
            
            user_id = decoded_token_payload["user_id"]
            email = decoded_token_payload["email"]
            session_id = decoded_token_payload["session_id"]

            # First delete the user session from the database
            user_session_collection = mongo_db_connection.get_collection("user_sessions")
            user_session_collection.delete_one({"user_id": user_id, "session_id": session_id})

            # Get the refresh token collection and delete the refresh token from the database
            refresh_tokens_collection = mongo_db_connection.get_collection("refresh_tokens")
            refresh_tokens_collection.delete_one({"user_id": user_id, "email": email})

            return JSONResponse(status_code=status.HTTP_200_OK, content={"status":"success", "message":"User logged out successfully!"})
        
        except Exception as e:
            return e
        
        finally:
            # Close the connection
            mongo_db_connection.close_connection()
            