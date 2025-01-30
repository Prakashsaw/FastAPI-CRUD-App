import os

from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


# Load environment variables from the .env file
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    """
    A class to manage application configuration using environment variables.
    It uses `pydantic.BaseSettings` for validation and dotenv for loading environment variables.

    Attributes:
        MONGO_URI (str): MongoDB connection URI.
        DB_NAME (str): MongoDB database name.
        JWT_ALGORITHM (str): Algorithm used for JWT tokens.
        JWT_ACCESS_SECRET_KEY (str): Secret key for signing access JWT tokens.
        JWT_ACCESS_EXPIRY_MINUTES (int): Expiry time for access JWT tokens in minutes.
        JWT_REFRESH_SECRET_KEY (str): Secret key for signing refresh JWT tokens.
        JWT_REFRESH_EXPIRY_DAYS (int): Expiry time for refresh JWT tokens in days.
        USER_SESSION_EXPIRY_MINUTES (int): Expiry time for user sessions in minutes.
        MAIL_USERNAME (str): Email service username.
        MAIL_PASSWORD (str): Email service password.
        MAIL_FROM (str): Sender email address.
        MAIL_FROM_NAME (str): Sender name.
        MAIL_PORT (int): Email service port.
        MAIL_SERVER (str): Email server address.
        MAIL_STARTTLS (bool): Whether to use STARTTLS for email.
        MAIL_SSL_TLS (bool): Whether to use SSL/TLS for email.
        USE_CREDENTIALS (bool): Whether to use credentials for email.
        VALIDATE_CERTS (bool): Whether to validate email server certificates.
        FRONTEND_HOST (str): Frontend application host URL.
        APP_NAME (str): Name of the application.
    """

    # Database settings
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "test_db")

    # JWT settings
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_SECRET_KEY: str = os.getenv("JWT_ACCESS_SECRET_KEY", "default_access_secret")
    JWT_ACCESS_EXPIRY_MINUTES: int = int(os.getenv("JWT_ACCESS_EXPIRY_MINUTES", 15))
    JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY", "default_refresh_secret")
    JWT_REFRESH_EXPIRY_DAYS: int = int(os.getenv("JWT_REFRESH_EXPIRY_DAYS", 7))

    USER_SESSION_EXPIRY_MINUTES: int = int(os.getenv("USER_SESSION_EXPIRY_MINUTES", 30))

    # Email settings
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "example@example.com")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "password")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "noreply@example.com")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "Example App")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", 587))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.example.com")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS", "True").lower() == "true"
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS", "False").lower() == "true"
    USE_CREDENTIALS: bool = os.getenv("USE_CREDENTIALS", "True").lower() == "true"
    VALIDATE_CERTS: bool = os.getenv("VALIDATE_CERTS", "True").lower() == "true"

    # Frontend settings
    FRONTEND_HOST: str = os.getenv("FRONTEND_HOST", "http://localhost:3000")
    APP_NAME: str = os.getenv("APP_NAME", "My FastAPI App")
