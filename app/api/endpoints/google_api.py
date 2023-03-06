from typing import Dict

from aiogoogle import Aiogoogle
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routers.entity_routers import google_router as router
from app.core.db import get_async_session
from app.core.google_client import URL_SPREADSHEETS, get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value
)


@router.post(
    '/',
    response_model=Dict[str, str],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
):
    """
    Receives data about closed projects, creates a table, grants access rights
    to the account, processes and writes data to the table, returns a link
    to the table.
    """
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid, projects, wrapper_services)
    return {'Url': URL_SPREADSHEETS + spreadsheetid}
