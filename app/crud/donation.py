from app.crud.base import CRUDBase
from app.models import Donation
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase[Donation, DonationCreate, None]):
    """
    Works with the donation table in the database.
    """

    pass


donation_crud = CRUDDonation(Donation)
