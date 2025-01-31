import logging

from fastapi import BackgroundTasks, HTTPException

from src.config.env_setting import Settings
from src.config.email_config import send_email


# Set up logging for better traceability
logger = logging.getLogger(__name__)


class EmailServices:
    """
    A class for email services, such as sending account verification and password reset emails.
    """
    def __init__(self):
        self.config = Settings()

    async def send_account_verification_email(self, user: dict, background_tasks: BackgroundTasks, activate_url: str):
        """
        Sends an account verification email to the user.
        """
        data = {
            'app_name': self.config.APP_NAME,
            "name": user["name"],
            'activate_url': activate_url
        }
        subject = f"Account Verification - {self.config.APP_NAME}"
        try:
            # Send the email asynchronously
            res = await send_email(
                recipients=[user["email"]],
                subject=subject,
                template_name="account-verification.html",
                context=data,
                background_tasks=background_tasks
            )
            return res
        except Exception as e:
            logger.error(f"Error sending account verification email to {user['email']}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error sending verification email")

    async def send_account_verification_confirmation_email(self, user: dict, background_tasks: BackgroundTasks):
        """
        Sends an account activation confirmation email to the user.
        """
        data = {
            'app_name': self.config.APP_NAME,
            "name": user["name"],
            'login_url': f'{self.config.FRONTEND_HOST}/login'
        }
        subject = f"Welcome - {self.config.APP_NAME}"
        try:
            # Send the email asynchronously
            res = await send_email(
                recipients=[user["email"]],
                subject=subject,
                template_name="account-verification-confirmation.html",
                context=data,
                background_tasks=background_tasks
            )
            return res
        except Exception as e:
            logger.error(f"Error sending account confirmation email to {user['email']}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error sending confirmation email")

    async def send_password_reset_email(self, user: dict, background_tasks: BackgroundTasks, reset_url: str):
        """
        Sends a password reset email to the user.
        """
        data = {
            'app_name': self.config.APP_NAME,
            "name": user["name"],
            'activate_url': reset_url,
        }
        subject = f"Reset Password - {self.config.APP_NAME}"
        try:
            # Send the email asynchronously
            res = await send_email(
                recipients=[user["email"]],
                subject=subject,
                template_name="password-reset.html",
                context=data,
                background_tasks=background_tasks
            )
            return res
        except Exception as e:
            logger.error(f"Error sending password reset email to {user['email']}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error sending password reset email")
        
    async def send_password_reset_confirmation_email(self, user: dict, background_tasks: BackgroundTasks):
        """
        Sends a password reset confirmation email to the user.
        """
        data = {
            'app_name': self.config.APP_NAME,
            "name": user["name"],
            'login_url': f'{self.config.FRONTEND_HOST}/login',
            'support_team_email': self.config.MAIL_FROM
        }
        subject = f"Password Reset Successful- {self.config.APP_NAME}"
        try:
            # Send the email asynchronously
            res = await send_email(
                recipients=[user["email"]],
                subject=subject,
                template_name="password-reset-confirmation.html",
                context=data,
                background_tasks=background_tasks
            )
            return res
        except Exception as e:
            logger.error(f"Error sending password reset confirmation email to {user['email']}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error sending password reset confirmation email")