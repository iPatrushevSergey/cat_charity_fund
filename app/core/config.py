from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """
    Defines the basic settings of the application. These settings
    are by default. Initially, these settings are checked in the
    operation system environment variables. It is also possible
    to directly access the .env file.
    """
    app_title: str = 'Cat charity fund'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    description: str = '## **API for the cat charity foundation**'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    mail_username: str = 'username',
    mail_password: str = '*********',
    mail_from: str = 'test@mail.com',
    mail_port: int = 465,
    mail_server: str = 'mail server',
    mail_from_name: str = 'from test mail',

    class Config:
        """
        Checks variables in the .env file.
        """
        env_file = '.env'


settings = Settings()
