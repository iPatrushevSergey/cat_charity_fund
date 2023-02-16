from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models import ProjectDonationBase


class Donation(ProjectDonationBase):
    """
    Model for creating donations. Inherits attributes
    BaseClass and ProjectDonationBase. Contains fields:
    -------------------------------------------------------
    id - integer primary key;
    full_amount - required amount for the project;
    invested_amount - the amount from the donation, which
    is distributed among the projects;
    fully_invested - whether all the money has been
    transferred;
    create_data - donation date;
    clode_data - date when the entire amount is distributed
    among projects;
    user_id - ID of the user who made the donation;
    comment - comments of the user who made the donation.
    -------------------------------------------------------
    """
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
