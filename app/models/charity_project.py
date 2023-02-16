from sqlalchemy import Column, String, Text

from app.models import ProjectDonationBase


class CharityProject(ProjectDonationBase):
    """
    Model for creating projects. Inherits attributes
    BaseClass and ProjectDonationBase. Contains fields:
    -------------------------------------------------------
    id - integer primary key;
    full_amount - required amount for the project;
    invested_amount - the amount contributed to the project;
    fully_invested - indicates whether the amount has been
    collected; create_data - project creation date;
    clode_data - project closing date;
    name - the project name;
    description - project description.
    -------------------------------------------------------
    """

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
