from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


class Investing:
    """
    Regulates the investment process.
    """
    def __init__(self, crud):
        """
        Initializes an object with the corresponding CRUD.
        """
        self.crud = crud

    async def invest(
        self,
        session: AsyncSession,
        created_object: Union[CharityProject, Donation]
    ):
        """
        Starts the investment process. If a CharityProject is received for
        input object, then Donation objects are requested from the database,
        and vice versa.
        """
        try:
            db_objects = await self.crud.get_by_attribute(
                'fully_invested', False, session, all_objects=True
            )
            if db_objects:
                index = 0
                number_of_db_objects = len(db_objects)

                while (not created_object.fully_invested and
                        index < number_of_db_objects):
                    db_object = db_objects[index]
                    created_obj_diff, db_obj_diff = (
                        self.counting_amounts(created_object, db_object))
                    if created_obj_diff > db_obj_diff:
                        db_object = self.close_object(db_object)
                        created_object.invested_amount += db_obj_diff
                        index += 1
                    elif created_obj_diff < db_obj_diff:
                        db_object.invested_amount += created_obj_diff
                        created_object = self.close_object(created_object)
                    elif created_obj_diff == db_obj_diff:
                        created_object = self.close_object(created_object)
                        db_object = self.close_object(db_object)
                    session.add(db_object)

            session.add(created_object)
        except Exception as error:
            await session.rollback()
            print(error)
        else:
            await session.commit()
            await session.refresh(created_object)
            return created_object

    def counting_amounts(self, created_object, db_object):
        """
        Calculates the difference between the required amount for the project
        and already invested, as well as the donation amount and the
        distributed amount.
        """
        created_obj_diff = (
            created_object.full_amount - created_object.invested_amount
        )
        db_obj_diff = db_object.full_amount - db_object.invested_amount
        return created_obj_diff, db_obj_diff

    def close_object(self, object):
        """
        When the indicator of the invested amount reaches the required amount
        or the distributed amount reaches the required donation amount, closes
        the project or donation.
        """
        object.invested_amount = object.full_amount
        object.fully_invested = True
        object.close_date = datetime.now()
        return object


invest_charity_project = Investing(donation_crud)
invest_donation = Investing(charity_project_crud)
