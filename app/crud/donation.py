from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    """
    Works with the donation table in the database.
    """

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession
    ) -> List[Donation]:
        """
        Returns all donation objects o a specific a user
        from the database.
        """
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
