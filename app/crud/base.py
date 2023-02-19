from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
PatchSchemaType = TypeVar('PatchSchemaType', bound=Optional[BaseModel])


class CRUDBase(Generic[ModelType, CreateSchemaType, PatchSchemaType]):
    """
    The base class for working with the database. The main methods
    are defined: get_all, create, get, update, delete.
    """

    def __init__(self, model: Type[ModelType]) -> None:
        """
        Initializes an object of the class with the attribute - model.
        """
        self.model = model

    async def get_all(self, session: AsyncSession) -> List[ModelType]:
        """
        Returns all objects of a specific model from the database.
        """
        db_objects = await session.scalars(select(self.model))
        return db_objects.all()

    async def create(
        self,
        object_in: CreateSchemaType,
        session: AsyncSession,
        user: Optional[User] = None,
    ) -> ModelType:
        """
        Converts a schema object into a hash-table, creates a model object
        in the database, updates the response object (taking into account
        the fields that was not in the request to create an object)
        and returns it.
        """
        object_in_data = object_in.dict()
        if user is not None:
            object_in_data['user_id'] = user.id
        db_object = self.model(**object_in_data)
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
        all_objects: bool = False,
    ) -> ModelType:
        """
        Returns by ID one object of a specific model from the database
        (if available), otherwise None.
        """
        attr = getattr(self.model, attr_name)
        db_object = await session.scalars(
            select(self.model).where(
                attr == attr_value
            )
        )
        if all_objects:
            return db_object.all()
        return db_object.first()

    async def patch(
        self,
        object_in: PatchSchemaType,
        db_object: ModelType,
        session: AsyncSession
    ) -> ModelType:
        """
        Converts a database object and schema object into hash-tables,
        checks the presence of fields in the data for object changes
        and if there are updates them. Saves the updated object to the
        database and updates the response object (taking into account
        the fields that were not in the request to update the object)
        and returns it.
        """
        object_data = jsonable_encoder(db_object)
        update_data = object_in.dict(exclude_unset=True)
        for field in object_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def delete(
        self,
        db_object: ModelType,
        session: AsyncSession
    ) -> ModelType:
        """
        Deletes an object from the database and returns it.
        """
        await session.delete(db_object)
        await session.commit()
        return db_object

    async def exists_object_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession
    ) -> Optional[bool]:
        """
        Checks the presence of an object in the database by attribute.
        """
        attr = getattr(self.model, attr_name)
        exists_criteria = (
            select(self.model).where(attr == attr_value).exists()
        )
        charity_project_exists = await session.scalars(
            select(True).where(exists_criteria)
        )
        return charity_project_exists.first()
