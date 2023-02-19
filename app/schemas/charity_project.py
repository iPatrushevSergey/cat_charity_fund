from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    """
    The basic scheme for the Charity Project. Defines fields
    and validates them.
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjectCreate(CharityProjectBase):
    """
    The scheme is necessary to create a charity project.
    """

    class Config:
        schema_extra = {
            'example': {
                'name': 'Кошкин дом',
                'description': 'Задача построить котану огромный дом',
                'full_amount': 10000
            }
        }


class CharityProjectUpdate(CharityProjectBase):
    """
    The scheme defines fields for updating data about a charity
    project and validates them.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100, example='Дом для кролика')
    description: Optional[str] = Field(None, example='Небольшой дом')
    full_amount: Optional[PositiveInt] = Field(None, example=5000)

    @validator('name')
    def name_cannot_be_null(cls, value: str):
        if value is None:
            raise ValueError(
                'The name of the charity project cannot be empty!'
            )
        return value


class CharityProjectDB(CharityProjectBase):
    """
    The scheme defines fields for responses to GET, POST, PATCH
    and DELETE requests.
    """
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        """
        The orm_mode attribute allows returning CharityProject
        objects from the database.
        """
        orm_mode = True
