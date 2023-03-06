from typing import List

from sqlalchemy import select
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate
)


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate,
    CharityProjectUpdate,
]):
    """
    Works with a table of charity project in the database.
    """
    async def get_projects_by_completion_rate(
            self, session: AsyncSession
    ) -> List[Row]:
        """
        Retrieves information about closed projects from the database
        and returns them.
        """
        completed_projects = await session.execute(
            select([CharityProject.name,
                    CharityProject.close_date,
                    CharityProject.create_date,
                    CharityProject.description]).where(
                CharityProject.fully_invested
            )
        )
        return completed_projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
