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

    pass


charity_project_crud = CRUDCharityProject(CharityProject)
