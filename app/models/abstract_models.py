from sqlalchemy import Column, int

from app.core.db import Base


class ProjectDonationBase(Base):
    __abstract__ = True
