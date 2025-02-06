import re

from fastapi import HTTPException, status, BackgroundTasks
from datetime import datetime, timezone

from src.config.database import MongoDBConnection
from src.serializers.user_serializer import individual_user_data
from src.config.security import PasswordManager
from src.utils.generate_unique_key import generate_unique_key
from src.config.jwt_token import JWTManager
from fastapi.responses import JSONResponse
from src.config.env_setting import Settings
from src.services.email_services import EmailServices


class UserControllersClass:
    def __init__(self):
        self.Config = Settings()
        self.mongo_db_connection = MongoDBConnection(self.Config.MONGO_URI, self.Config.DB_NAME)
        self.email_services = EmailServices()
        self.password_manager = PasswordManager()
        self.jwt_manager = JWTManager()
        self.email_regex_parrern = r"^(?!.*\.\.)[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"

    def _start_connection(self):
        """
        Start the MongoDB connection.
        """
        self.mongo_db_connection.start_connection()

    def _get_collection(self, collection_name: str):
        """
        Helper method to get MongoDB collection.
        """
        # self.mongo_db_connection.start_connection()
        return self.mongo_db_connection.get_collection(collection_name)

    def _close_connection(self):
        """
        Helper method to close MongoDB connection.
        """
        self.mongo_db_connection.close_connection()

    def _validate_signup_input(self, user):
        """
        Validate the user input for the signup process.
        """
        if not all([user.get("name"), user.get("email"), user.get("password")]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields are required!")

        if user["name"] == "" or user["email"] == "" or user["password"] == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields are required!")

        if not re.match(self.email_regex_parrern, user["email"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format!")

        if not self.password_manager.is_password_strong_enough(user["password"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a strong password.")

    def _validate_login_input(self, user):
        """
        Validate the user input for the login process.
        """
        if not user.get("email") or not user.get("password"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields are required!")
        
    async def _send_verification_email(self, user_payload, background_tasks):
        """
        Helper method to send the email verification.
        """
        payload = {"user_id": user_payload["user_id"], "email": user_payload["email"]}
        email_verification_token = self.jwt_manager.create_access_token(payload)
        activate_url = f"{self.Config.FRONTEND_HOST}/user-auth/account-verify?token={email_verification_token}&email={user_payload['email']}"
        
        res = await self.email_services.send_account_verification_email(user_payload, background_tasks, activate_url)
        if not res:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send account verification email!")

    async def _handle_unverified_user(self, fetched_user, background_tasks):
        """
        Handle the case where the user is not verified yet.
        """
        payload = {"user_id": fetched_user["user_id"], "email": fetched_user["email"]}
        email_verification_token = self.jwt_manager.create_access_token(payload)
        activate_url = f"{self.Config.FRONTEND_HOST}/user-auth/account-verify?token={email_verification_token}&email={fetched_user['email']}"
        
        res = await self.email_services.send_account_verification_email(fetched_user, background_tasks, activate_url)
        if not res:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send account verification email!")
        
        return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "failed", "message": "User is not verified! Please check your email and verify your account.", "user": individual_user_data(fetched_user)})
    
    async def _handle_login_success(self, fetched_user):
        """
        Handle the successful login and generate JWT access and refresh tokens.
        """
        session_id = generate_unique_key()

        # Create JWT tokens
        jwt_payload = {"user_id": fetched_user["user_id"], "email": fetched_user["email"], "session_id": session_id}
        jwt_access_token = self.jwt_manager.create_access_token(jwt_payload)
        jwt_refresh_token = self.jwt_manager.create_refresh_token(jwt_payload)

        # Store session and refresh token in the database
        self._store_user_session(fetched_user, session_id)
        self._store_refresh_token(fetched_user, jwt_refresh_token)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "message": "User logged in successfully!",
                "user": individual_user_data(fetched_user),
                "jwt_access_token": jwt_access_token,
                "jwt_refresh_token": jwt_refresh_token,
            }
        )

    def _store_user_session(self, fetched_user, session_id):
        """
        Store the user session in the database.
        """
        user_session_collection = self._get_collection("user_sessions")
        user_session_payload = {"session_id": session_id, "user_id": fetched_user["user_id"], "email": fetched_user["email"]}
        user_session_collection.insert_one(user_session_payload)

    def _store_refresh_token(self, fetched_user, jwt_refresh_token):
        """
        Store the refresh token in the database.
        """
        refresh_token_collection = self._get_collection("refresh_tokens")
        refresh_token_collection.delete_many({"user_id": fetched_user["user_id"], "email": fetched_user["email"]})
        refresh_token_collection.insert_one({"user_id": fetched_user["user_id"], "email": fetched_user["email"], "refresh_token": jwt_refresh_token})


    async def signup_user(self, user: dict, background_tasks: BackgroundTasks):
        """
        Handle the user signup process by validating the input, creating a new user, and sending the email verification link.
        """
        try:
            self._start_connection()

            user = dict(user)

            # Validation checks
            self._validate_signup_input(user)

            # Get the user collection
            user_collection = self._get_collection("users")

            # Check if user already exists
            if user_collection.find_one({"email": user["email"]}):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists!")

            # Generate unique user ID and hashed password
            unique_id = generate_unique_key()
            hashed_password = self.password_manager.encode_and_hash_password(user["password"])
            user_payload = {
                "user_id": unique_id,
                "name": user["name"],
                "email": user["email"],
                "password": hashed_password,
                "is_verified": False,
                "created_at": str(datetime.now(timezone.utc)),
                "updated_at": str(datetime.now(timezone.utc))
            }

            # Send email verification
            await self._send_verification_email(user_payload, background_tasks)

            # Insert user into the database
            new_user = user_collection.insert_one(user_payload)
            if new_user.inserted_id is None:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User not created!")

            created_user = user_collection.find_one({"user_id": user_payload["user_id"]})

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"status": "success", "message": "User created successfully. Please check your email box and verify your account.", "user": individual_user_data(created_user)}
            )

        except Exception as e:
            raise e
        finally:
            self._close_connection()

    async def login_user(self, user: dict, background_tasks: BackgroundTasks):
        """
        Handle the user login process by validating the input, checking the user credentials, and generating JWT tokens.
        """
        try:
            self._start_connection()

            user = dict(user)

            # Validation checks
            self._validate_login_input(user)

            # Get the user collection
            user_collection = self._get_collection("users")
            fetched_user = user_collection.find_one({"email": user["email"]})

            if not fetched_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist!")

            if not self.password_manager.verify_password(user["password"], fetched_user["password"]):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect!")

            if not fetched_user.get("is_verified"):
                return await self._handle_unverified_user(fetched_user, background_tasks)

            # Handle user session and tokens
            return await self._handle_login_success(fetched_user)

        except Exception as e:
            raise e
        finally:
            self._close_connection()

    async def user_account_verification_controller(self, token: str, background_tasks: BackgroundTasks):
        """
        Handle user account verification by decoding the token and updating the verification status.

        Args:
            token (str): The token sent to the user's email for verification.
            background_tasks (BackgroundTasks): Background task manager for sending emails.
        """
        try:
            self._start_connection()

            # Validate and decode the token
            decoded_data_dict = self.jwt_manager.decode_token(token, is_refresh=False)
            if decoded_data_dict.get("error"):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=decoded_data_dict["error"])

            user_id = decoded_data_dict["user_id"]
            email = decoded_data_dict["email"]

            # Get the user collection
            user_collection = self._get_collection("users")
            user = user_collection.find_one({"user_id": user_id, "email": email})
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

            if user.get("is_verified"):
                return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "success", "message": "User account already verified. Login to continue."})
            
            # Update user verification status
            user_collection.find_one_and_update({"user_id": user_id, "email": email}, {"$set": {"is_verified": True}})

            # Send account activation confirmation email
            res = await self.email_services.send_account_verification_confirmation_email(user, background_tasks)
            if not res:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send account activation confirmation email!")

            return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "success", "message": "User account verified successfully. Login to continue."})

        except Exception as e:
            raise e
        finally:
            self._close_connection()

    async def refresh_token_controller(self, decoded_token_payload: dict):
        """
        Handle the refresh token request by verifying the user session and generating new tokens.

        Args:
            decoded_token_payload (dict): The decoded JWT token payload.
        """
        try:
            self._start_connection()

            user_id = decoded_token_payload["user_id"]
            email = decoded_token_payload["email"]
            session_id = decoded_token_payload["session_id"]

            # Check if the user session exists
            user_session_collection = self._get_collection("user_sessions")
            user_session = user_session_collection.find_one({"user_id": user_id, "session_id": session_id})
            if user_session is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User session is not valid! Please login again to continue.")

            # Generate new access token and refresh token
            jwt_payload = {"user_id": user_id, "email": email, "session_id": session_id}
            jwt_access_token = self.jwt_manager.create_access_token(jwt_payload)

            # Fetch the refresh token from the database
            refresh_tokens_collection = self._get_collection("refresh_tokens")
            refresh_token_store = refresh_tokens_collection.find_one({"user_id": user_id, "email": email})
            if refresh_token_store is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token!")

            jwt_refresh_token = refresh_token_store["refresh_token"]

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"status": "success", "message": "Access token refreshed successfully!", "jwt_access_token": jwt_access_token, "jwt_refresh_token": jwt_refresh_token, "session_id": session_id}
            )

        except Exception as e:
            raise e
        finally:
            self._close_connection()

    async def logout_user(self, token: str):
        """
        Handle the user logout by deleting the user session and refresh token.

        Args:
            decoded_token_payload (dict): The decoded JWT token payload.
        """
        try:
            self._start_connection()

            decoded_token_payload = self.jwt_manager.decode_jwt_token_without_expirytime(token)
            
            user_id = decoded_token_payload["user_id"]
            email = decoded_token_payload["email"]
            session_id = decoded_token_payload["session_id"]

            # Delete the user session
            user_session_collection = self._get_collection("user_sessions")
            user_session_collection.delete_one({"user_id": user_id, "session_id": session_id})

            # Delete the refresh token
            refresh_tokens_collection = self._get_collection("refresh_tokens")
            refresh_tokens_collection.delete_one({"user_id": user_id, "email": email})

            return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "success", "message": "User logged out successfully!"})

        except Exception as e:
            raise e
        finally:
            self._close_connection()

    async def send_password_reset_email_controller(self, email: str, background_tasks: BackgroundTasks):
        """
        Handle the forgot password email request by sending the reset password link.

        Args:
            email (str): The user's email address.
            background_tasks (BackgroundTasks): Background task manager for sending emails.

        Returns:
            JSONResponse: The response message.
        """
        try:
            self._start_connection()

            if not email or email == "":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is required!")
            
            user_collection = self._get_collection("users")
            user = user_collection.find_one({"email": email})
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist!")

            # Generate the reset password token
            payload = {"user_id": user["user_id"], "email": user["email"]}
            reset_password_token = self.jwt_manager.create_access_token(payload)
            reset_password_url = f"{self.Config.FRONTEND_HOST}/user-auth/reset-password?token={reset_password_token}&email={user['email']}"

            # Send the reset password email
            res = await self.email_services.send_password_reset_email(user, background_tasks, reset_password_url)
            if not res:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send reset password email!")

            return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "success", "message": "Reset password link sent successfully. Please check your email."})

        except Exception as e:
            raise e
        finally:
            self._close_connection()

    async def password_reset_controller(self, token: str, new_password: str, background_tasks: BackgroundTasks):
        """
        Handle the password reset process by decoding the token and updating the user's password.

        Args:
            token (str): The reset password token.
            new_password (str): The new password.
            background_tasks (BackgroundTasks): Background task manager for sending emails.

        Returns:
            JSONResponse: The response message.
        """
        try:
            self._start_connection()
            
            if not new_password or new_password == "":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password is required!")
            
            # Validate and decode the token
            decoded_data_dict = self.jwt_manager.decode_token(token, is_refresh=False)
            if decoded_data_dict.get("error"):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=decoded_data_dict["error"])

            user_id = decoded_data_dict["user_id"]
            email = decoded_data_dict["email"]

            # Get the user collection
            user_collection = self._get_collection("users")
            user = user_collection.find_one({"user_id": user_id, "email": email})
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist!")

            # Update the user's password
            hashed_password = self.password_manager.encode_and_hash_password(new_password)
            user_collection.find_one_and_update({"user_id": user_id, "email": email}, {"$set": {"password": hashed_password}})

            # Send password reset confirmation email
            res = await self.email_services.send_password_reset_confirmation_email(user, background_tasks)
            if not res:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send password reset confirmation email!")

            return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "success", "message": "Password reset successfully. Login to continue."})

        except Exception as e:
            raise e
        finally:
            self._close_connection()
