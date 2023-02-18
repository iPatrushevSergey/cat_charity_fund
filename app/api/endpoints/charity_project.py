from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists, check_name_duplicate, check_invested_amount,
    check_fully_invested, check_amount_not_less_than_nested
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)

router = APIRouter()


@router.get(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Returns all charity project objects with all model fields CharityProject.
    If the project is not closed, excludes the empty `close_date` field.
    """
    return await charity_project_crud.get_all(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Checks whether there is a charity project with this name, creates project
    and returns an object with all fields, excluding the `close_date` field.
    Only superuser is available.
    """
    await check_name_duplicate(charity_project.name, session)
    return await charity_project_crud.create(charity_project, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    object_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Checks the existence of the charity project and its name. Checks
    the change in the required amount of the project - whether it is less
    than the already invested amount or not. Updates the project fields
    and returns the object with all fields. If the project is not closed,
    excludes the empty `close_date` field. Only superuser is available.
    """
    charity_project = await check_charity_project_exists(project_id, session)
    if charity_project.name is not None:
        await check_name_duplicate(object_in.name, session)
    check_fully_invested(charity_project)
    if object_in.full_amount:
        await check_amount_not_less_than_nested(
            charity_project, object_in.full_amount
        )
    return await charity_project_crud.patch(
        object_in, charity_project, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Checks the existence of a charity project, investment in the funds
    project. Deletes the project and returns it. If the project not closed,
    excludes the empty `close_date` field. Only superuser is available.
    """
    charity_project = await check_charity_project_exists(project_id, session)
    check_invested_amount(charity_project)
    return await charity_project_crud.delete(charity_project, session)
