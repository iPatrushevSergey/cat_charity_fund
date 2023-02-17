from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class CharityProjectBase(BaseModel):
    """
    The basic scheme for the Charity Project. Defines fields
    and validates them.
    """
    name: str = Field(..., min_length=1, max_length=100)
    descriptoin: str
    full_amount: PositiveInt


class CharityProjectCreate(CharityProjectBase):
    """
    The scheme is necessary to create a charity project.
    """
    pass


class CharityProjectUpdate(CharityProjectBase):
    """
    The scheme defines fields for updating data about a charity
    project and validates them.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    descriptoin: Optional[str]
    full_amount: Optional[PositiveInt]


class CharityProjectDB(CharityProjectBase):
    """
    The scheme defines fields for responses to GET, POST, PATCH
    and DELETE requests.
    """
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime

    class Config:
        """
        The orm_mode attribute allows returning CharityProject
        objects from the database.
        """
        orm_mode = True
