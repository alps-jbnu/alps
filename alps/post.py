from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, Integer, String, Text

from alps.db import Base
from alps.user import MemberType, User

__all__ = 'Board', 'Post'


class Board(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    text = Column(String(100), nullable=False)
    read_permission = Column(Integer, nullable=False,
                             default=MemberType.non_member.value,
                             server_default='0')
    write_permission = Column(Integer, nullable=False,
                              default=MemberType.non_member.value,
                              server_default='0')

    posts = relationship('Post',
                         cascade='all, delete-orphan',
                         lazy='dynamic')

    created_at = Column(DateTime(timezone=True), nullable=False,
                        default=now())

    __tablename__ = 'boards'


class Post(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), index=True, nullable=False)
    content = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship(User)

    board_id = Column(Integer, ForeignKey(Board.id), nullable=False)
    board = relationship(Board)

    created_at = Column(DateTime(timezone=True), nullable=False,
                        default=now())

    __tablename__ = 'posts'
