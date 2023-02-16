from sqlalchemy import Column, String, Text

from app.models import ProjectDonationBase


class CharityProject(ProjectDonationBase):

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
