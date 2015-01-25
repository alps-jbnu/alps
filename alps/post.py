from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, Integer, String, Text

from alps.db import Base
from alps.user import User

__all__ = 'Post',


class Post(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User)

    created_at = Column(DateTime(timezone=True), nullable=False,
                        default=now())

    __tablename__ = 'posts'
