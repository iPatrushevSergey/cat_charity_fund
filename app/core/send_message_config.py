# Module with the email sending settings.
from fastapi_mail import ConnectionConfig, MessageSchema, MessageType

from app.core.config import settings


def generates_message(email: str, html: str, subject: str) -> MessageSchema:
    """
    Returns the scheme of the response letter. Accepts
    the mailbox to which the response and the content
    of the response.
    """
    return MessageSchema(
        subject=subject,
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )


send_message_config = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    MAIL_FROM_NAME=settings.mail_from_name,
    USE_CREDENTIALS=True,
)

registration_html = """
    <p>Thank you for registering with the cat charity foundation</p>
    """

registration_subject = 'You have succesfully registered'
