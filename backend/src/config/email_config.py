import os

from fastapi import HTTPException, status
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from fastapi.background import BackgroundTasks

from src.config.env_setting import Settings


# Load environment settings
Config = Settings()


# Configure email connection
conf = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_PORT=Config.MAIL_PORT,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_STARTTLS=Config.MAIL_STARTTLS,
    MAIL_SSL_TLS=Config.MAIL_SSL_TLS,
    USE_CREDENTIALS=Config.USE_CREDENTIALS,
    VALIDATE_CERTS=Config.VALIDATE_CERTS,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
)


async def send_email(
    recipients: list, subject: str, context: dict, template_name: str, background_tasks: BackgroundTasks
):
    """
    Send an email using the provided template and context.

    Args:
        recipients (list): List of recipient email addresses.
        subject (str): Subject of the email.
        context (dict): Context data for the email template.
        template_name (str): Name of the email template.
        background_tasks (BackgroundTasks): Background task manager to send the email asynchronously.

    Returns:
        bool: True if the email is sent successfully.

    Raises:
        HTTPException: If the email fails to send.
    """
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=context,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    try:
        background_tasks.add_task(fm.send_message, message, template_name=template_name)
        print("Email has been sent successfully!")
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send email: {str(e)}",
        )

async def test_fastmail():
    """
    Test the FastMail email sending functionality.

    Returns:
        bool: True if the test email is sent successfully.

    Raises:
        Exception: If the test email fails to send.
    """
    message = MessageSchema(
        subject="Test Email",
        recipients=["prakash1999saw@gmail.com"],
        template_body={
            "app_name": "FastAPI CRUD App",
            "name": "Test User",
            "activate_url": "http://example.com",
        },
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message, template_name="account-verification.html")
        print("Test email sent successfully!")
        return True
    except Exception as e:
        print(f"Error in test email: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send test email: {str(e)}",
        )












# import os
# from fastapi import HTTPException, status
# from pathlib import Path
# from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
# from fastapi.background import BackgroundTasks
# from src.config.env_setting import Settings

# Config = Settings()

# # Email Configuration
# conf = ConnectionConfig(
#     MAIL_USERNAME = Config.MAIL_USERNAME,
#     MAIL_PASSWORD = Config.MAIL_PASSWORD,
#     MAIL_FROM = Config.MAIL_FROM,
#     MAIL_FROM_NAME = Config.MAIL_FROM_NAME,
#     MAIL_PORT = Config.MAIL_PORT,
#     MAIL_SERVER = Config.MAIL_SERVER,
#     MAIL_STARTTLS = Config.MAIL_STARTTLS,
#     MAIL_SSL_TLS = Config.MAIL_SSL_TLS,
#     USE_CREDENTIALS = Config.USE_CREDENTIALS,
#     VALIDATE_CERTS = Config.VALIDATE_CERTS,
#     TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
# )

# async def send_email(recipients: list, subject: str, context: dict, template_name: str, background_tasks: BackgroundTasks):
#     message = MessageSchema(
#         subject=subject,
#         recipients=recipients,
#         template_body=context,
#         subtype=MessageType.html
#     )

#     fm = FastMail(conf)
#     try:
#         background_tasks.add_task(fm.send_message, message, template_name=template_name)
#         print("message1: ", "Email has been sent successfully!")
#         return True
#     except Exception as e:
#         print(f"Error1: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to send email: {str(e)}"
#         )
    
# async def test_fastmail():
#     message = MessageSchema(
#         subject="Test Email",
#         recipients=["prakash1999saw@gmail.com"],
#         template_body={"app_name": "FastAPI CRUD App", "name": "Test User", "activate_url": "http://example.com"},
#         subtype=MessageType.html,
#     )

#     fm = FastMail(conf)
#     try:
#         await fm.send_message(message, template_name="account-verification.html")
#         # background_tasks.add_task(fm.send_message, message, template_name="account-verification.html")
#         print("Email sent successfully!")
#         return True
#     except Exception as e:
#         print(f"FastMail error: {e}")
#         raise e
    

