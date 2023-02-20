from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession,
) -> None:
    """
    Checks the duplicate name of the charity project. If the name exists,
    it returns an exception.
    """
    charity_project_exists = await (
        charity_project_crud.exists_object_by_attribute(
            'name', charity_project_name, session
        )
    )
    if charity_project_exists:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """
    Checks the existence of a charity project. If it does not exist,
    it returns an exception.
    """
    charity_project = await charity_project_crud.get_by_attribute(
        'id', charity_project_id, session
    )
    if not charity_project:
        raise HTTPException(status_code=404, detail='Charity fund not found')
    return charity_project


def check_invested_amount(charity_project: CharityProject) -> None:
    """
    Checks the investment of money in a charity project. If invested, returns
    an exception.
    """
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


def check_fully_invested(charity_project: CharityProject) -> None:
    """
    Checks the closure of the charity project. If closed, return an exception.
    """
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400, detail='Закрытый проект нельзя редактировать!'
        )


def check_amount_not_less_than_nested(
    charity_project: CharityProject,
    new_full_amount: int,
) -> None:
    """
    Checks the required amount to be set. If it is smaller than the already
    nested one, it returns an exception.
    """
    if new_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=422,
            detail='It is impossible to set the required amount less than '
                   'the amount alredy invested'
        )


def check_empty_fields(object_in: CharityProjectUpdate):
    """
    Checss all fields for an empty value at the same time.
    """
    if not object_in.dict(exclude_unset=True):
        raise HTTPException(
            status_code=422,
            detail='All fields cannot be empty at the same time'
        )
