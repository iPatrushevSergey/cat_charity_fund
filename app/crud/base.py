from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    """
    The base class for working with the database. The main methods
    are defined: get_all, create, get, update, delete.
    """

    def __init__(self, model):
        """
        Initializes an object of the class with the attribute - model.
        """
        self.model = model

    async def get_all(self, session: AsyncSession):
        """
        Returns all objects of a specific model from the database.
        """
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def create(self, object_in, session: AsyncSession):
        """
        Converts a schema object into a hash-table, creates a model object
        in the database, updates the response object (taking into account
        the fields that was not in the request to create an object)
        and returns it.
        """
        object_in_data = object_in.dict()
        db_object = self.model(**object_in_data)
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def get(self, object_id: int, session: AsyncSession):
        """
        Returns by ID one object of a specific model from the database
        (if available), otherwise None.
        """
        db_object = await session.execute(
            select(self.model).where(
                self.model.id == object_id
            )
        )
        return db_object.scalars().first()

    async def patch(self, object_in, db_object, session: AsyncSession):
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

    async def delete(self, db_object, session: AsyncSession):
        """
        Deletes an object from the database and returns it.
        """
        await session.delete(db_object)
        await session.commit()
        return db_object
