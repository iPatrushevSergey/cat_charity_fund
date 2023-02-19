from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationCreate(BaseModel):
    """
    The scheme defines the fields for creating donations and validates them.
    """
    full_amount: PositiveInt = Field(..., example=3000)
    comment: Optional[str] = Field(None, example='Деньги на дом котану')


class DonationGetCreateDB(DonationCreate):
    """
    The schema defines fields for responses to POST and `Get User Donations`
    requests.
    """
    id: int
    create_date: datetime

    class Config:
        """
        The orm_mode attribute allows returning CharityProject
        objects from the database.
        """
        orm_mode = True


class DonationGetDB(DonationGetCreateDB):
    """
    The schema defines the fields for responding to the `Get All Donations`
    request.
    """
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
