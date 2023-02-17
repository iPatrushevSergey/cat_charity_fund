from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationCreate(BaseModel):
    """
    The scheme defines the fields for creating donations and validates them.
    """
    full_amount: PositiveInt
    comment: Optional[str]


class DonationGetCreatedDB(DonationCreate):
    """
    The schema defines fields for responses to POST and `Get User Donations`
    requests.
    """
    id: int
    create_date: datetime


class DonationGetDB(DonationGetCreatedDB):
    """
    The schema defines the fields for responding to the `Get All Donations`
    request.
    """
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
