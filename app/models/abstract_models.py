from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class ProjectDonationBase(Base):
    """
    Abstract model. Inherits attributes BaseClass.
    The descriptions of the fields is contained in the child
    models, since their specifications is different.
    """
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
