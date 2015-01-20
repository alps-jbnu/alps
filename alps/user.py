from sqlalchemy.schema import Column
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, Integer, String

from alps.db import Base

__all__ = 'User',


class User(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False,
                        default=now())

    __tablename__ = 'users'
