from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession,
) -> None:
    charity_project_id = await (
        charity_project_crud.get_charity_project_by_name(
            charity_project_name, session
        )
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='A charity project with that name already exists'
        )
