from app.crud.base import CRUDBase
from app.models import Donation


class CRUDDonation(CRUDBase):
    """
    Works with the donation table in the database.
    """

    pass


donation_crud = CRUDDonation(Donation)
