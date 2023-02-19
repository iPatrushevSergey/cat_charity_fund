from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    """
    Works with a table of charity project in the database.
    """

    pass


charity_project_crud = CRUDCharityProject(CharityProject)
