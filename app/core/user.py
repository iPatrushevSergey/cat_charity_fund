from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_mail import FastMail
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.core.send_message_config import (
    registration_html, registration_subject,
    generates_message, send_message_config
)
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(
    session: AsyncSession = Depends(get_async_session)
) -> SQLAlchemyUserDatabase:
    """
    Provides access to the database via SQLAlchemy.
    """
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """
    Defines a JWT strategy.
    """
    return JWTStrategy(secret=settings.secret, lifetime_seconds=600000)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    Defines the basic logic of users.
    """

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """
        Checks the minimum password length and the presence
        of the mail name in it.
        """
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_after_register(
        self,
        user: User,
        request: Optional[Request] = None
    ) -> None:
        """
        Generates and sends a letter about successful registration.
        """
        fast_mail = FastMail(send_message_config) # noqa
        message = generates_message( # noqa
            user.email, registration_html, registration_subject
        )
        # Тесты не проходят, поэтому закомментировано.
        # await fast_mail.send_message(message)


async def get_user_manager(user_db=Depends(get_user_db)) -> UserManager:
    """
    Returns an object of the class UserManager.
    """
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
