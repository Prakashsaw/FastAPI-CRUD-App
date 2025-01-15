from fastapi import BackgroundTasks
from src.config.env_setting import Config
from src.models.user_model import User
from src.config.email import send_email
from src.utils.email_context import USER_VERIFY_ACCOUNT, FORGOT_PASSWORD
from src.config.security import encode_and_hash_password



async def send_account_verification_email(user: User, background_tasks: BackgroundTasks, activate_url: str):
    # string_context = user.get_context_string(context=USER_VERIFY_ACCOUNT)
    # token = encode_and_hash_password(string_context)
    # activate_url = f"{Config.FRONTEND_HOST}/auth/account-verify?token={token}&email={user.email}"
    data = {
        'app_name': Config.APP_NAME,
        "name": user["name"],
        'activate_url': activate_url
    }
    subject = f"Account Verification - {Config.APP_NAME}"
    await send_email(
        recipients=[user["email"]],
        subject=subject,
        template_name="user_email/account-verification.html",
        context=data,
        background_tasks=background_tasks
    )
    
    
async def send_account_activation_confirmation_email(user: User, background_tasks: BackgroundTasks):
    data = {
        'app_name': Config.APP_NAME,
        "name": user["name"],
        'login_url': f'{Config.FRONTEND_HOST}'
    }
    subject = f"Welcome - {Config.APP_NAME}"
    await send_email(
        recipients=[user["email"]],
        subject=subject,
        template_name="user_email/account-verification-confirmation.html",
        context=data,
        background_tasks=background_tasks
    )
    
async def send_password_reset_email(user: User, background_tasks: BackgroundTasks, reset_url: str):
    # string_context = user.get_context_string(context=FORGOT_PASSWORD)
    # token = encode_and_hash_password(string_context)
    # reset_url = f"{Config.FRONTEND_HOST}/reset-password?token={token}&email={user.email}"
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