from datetime import datetime
from typing import List

from aiogoogle import Aiogoogle
from sqlalchemy.engine.row import Row

from app.core.config import settings
from app.core.google_client import FORMAT


async def spreadsheets_create(wrapper_service: Aiogoogle) -> str:
    """
    Creates a table with the specified parameters and returns
    the ID the created document.
    """
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_service.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчёт на {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 10}}}]
    }
    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapeer_service: Aiogoogle,
) -> None:
    """
    Grants access rights to the specified account to the created document.
    """
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapeer_service.discover('drive', 'v3')
    await wrapeer_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id',
        )
    )


async def spreadsheets_update_value(
        spreadsheetid: str,
        completed_projects: List[Row],
        wrapper_services: Aiogoogle,
) -> None:
    """
    Processes and writes to the table the information received
    from the database.
    """
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'],
    ]
    rows = []
    for project in completed_projects:
        collection_period = project['close_date'] - project['create_date']
        new_row = [project['name'], collection_period, project['description']]
        rows.append(new_row)
    rows.sort(key=lambda row: row[1])
    for row in rows:
        row[1] = str(row[1])
    table_values += rows
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values,
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E50',
            valueInputOption='USER_ENTERED',
            json=update_body,
        )
    )
