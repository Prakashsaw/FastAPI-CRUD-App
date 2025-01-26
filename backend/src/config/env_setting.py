import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    # Database settings
    MONGO_URI: str = os.getenv("MONGO_URI")
    DB_NAME: str = os.getenv("DB_NAME")

    # JWT settings
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    JWT_ACCESS_SECRET_KEY: str = os.getenv("JWT_ACCESS_SECRET_KEY")
    JWT_ACCESS_EXPIRY_MINUTES: int = os.getenv("JWT_ACCESS_EXPIRY_MINUTES")
    JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY")
    JWT_REFRESH_EXPIRY_DAYS: int = os.getenv("JWT_REFRESH_EXPIRY_DAYS")

    USER_SESSION_EXPIRY_MINUTES: int = os.getenv("USER_SESSION_EXPIRY_MINUTES")
    
    # REDIS_URL: str = "redis://localhost:6379/0"

    # Email settings
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME")
    MAIL_PORT: int = os.getenv("MAIL_PORT")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS")
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS")
    USE_CREDENTIALS: bool = os.getenv("USE_CREDENTIALS")
    VALIDATE_CERTS: bool = os.getenv("VALIDATE_CERTS")
    # DOMAIN: str

    # Frontend url
    FRONTEND_HOST: str = os.getenv("FRONTEND_HOST")
    APP_NAME: str = os.getenv("APP_NAME")
    # model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")

