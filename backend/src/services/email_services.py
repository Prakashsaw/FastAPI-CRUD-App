from fastapi import BackgroundTasks
from src.config.env_setting import Settings
from src.schemas.user_schema import User
from src.config.email_config import send_email
from src.utils.email_context import USER_VERIFY_ACCOUNT, FORGOT_PASSWORD


class EmailServices:
    # Initialize the class
    def __init__(self):
        pass

    # Send account verification email
    async def send_account_verification_email(self, user: dict, background_tasks: BackgroundTasks, activate_url: str):
        Config = Settings()
        data = {
            'app_name': Config.APP_NAME,
            "name": user["name"],
            'activate_url': activate_url
        }
        subject = f"Account Verification - {Config.APP_NAME}"
        try:
            res = await send_email(
                recipients=[user["email"]],
                subject=subject,
                template_name="account-verification.html",
                context=data,
                background_tasks=background_tasks
            )
            return res
        except Exception as e:
            # print("Error2:", e)
            raise e
        
    # Send account activation confirmation email
    async def send_account_verification_confirmation_email(self, user: dict, background_tasks: BackgroundTasks):
        Config = Settings()
        data = {
            'app_name': Config.APP_NAME,
            "name": user["name"],
            'login_url': f'{Config.FRONTEND_HOST}/login'
        }
        subject = f"Welcome - {Config.APP_NAME}"
        try:
            res = await send_email(
                recipients=[user["email"]],
                subject=subject,
                template_name="account-verification-confirmation.html",
                context=data,
                background_tasks=background_tasks
            )
            return res
        except Exception as e:
            # print("Error3:", e)
            raise e
        
    # Send password reset email
    async def send_password_reset_email(self, user: dict, background_tasks: BackgroundTasks, reset_url: str):
        # string_context = user.get_context_string(context=FORGOT_PASSWORD)
        # token = encode_and_hash_password(string_context)
        # reset_url = f"{Config.FRONTEND_HOST}/reset-password?token={token}&email={user.email}"
        Config = Settings()
        data = {
            'app_name': Config.APP_NAME,
            "name": user["name"],
            'activate_url': reset_url,
        }
        subject = f"Reset Password - {Config.APP_NAME}"
        await send_email(
            recipients=[user["email"]],
            subject=subject,
            template_name="user_email/password-reset.html",
            context=data,
            background_tasks=background_tasks
        )