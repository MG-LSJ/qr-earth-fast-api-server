from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import Config
from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent

email_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USRNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM_EMAIL,
    MAIL_PORT=587,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

mail_client = FastMail(
    config=email_config,
)


def create_message(recipients: list[str], subject: str, body: str):
    return MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.plain,
    )
