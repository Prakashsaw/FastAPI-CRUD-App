import os
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from fastapi.background import BackgroundTasks
from src.config.env_setting import Config

conf = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_PORT=Config.MAIL_PORT,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_STARTTLS=Config.MAIL_STARTTLS,
    MAIL_SSL_TLS=Config.MAIL_SSL_TLS,
    MAIL_DEBUG=True,
    MAIL_FROM=Config.MAIL_FROM,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
    USE_CREDENTIALS=True,
)

fm = FastMail(conf)


async def send_email(recipients: list, subject: str, context: dict, template_name: str, background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=context,
        subtype=MessageType.html
    )

    background_tasks.add_task(fm.send_message, message, template_name=template_name)