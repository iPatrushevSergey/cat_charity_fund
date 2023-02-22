from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routers.entity_routers import donation_router as router
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate, DonationGetCreateDB, DonationGetDB
)
from app.services.investment_process import invest_donation


@router.get(
    '/',
    response_model=List[DonationGetDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Returns all donations. If the project is not closed, excludes
    the empty `close_date` field. Only superuser is available.
    """
    return await donation_crud.get_all(session)


@router.post(
    '/',
    response_model=DonationGetCreateDB,
    response_model_exclude_none=True,
)
async def create_donation(
    object_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),

):
    """
    Creates a donation. Available only to an authorized user.
    """
    donation = await donation_crud.create(object_in, session, user)
    return await invest_donation.invest(session, donation)


@router.get(
    '/my',
    response_model=List[DonationGetCreateDB],
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Returns all donations of a specific user. Available only
    to an authorized user.
    """
    return await donation_crud.get_by_attribute(
        'user_id', user.id, session, all_objects=True
    )
