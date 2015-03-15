import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, Integer, String, Text

from alps.db import Base
from alps.user import MemberType, User

__all__ = 'Board', 'Post'


class Board(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), index=True, nullable=False, unique=True)
    text = Column(String(100), nullable=False)
    read_permission = Column(Integer, nullable=False,
                             default=MemberType.non_member.value)
    write_permission = Column(Integer, nullable=False,
                              default=MemberType.non_member.value)

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

    user_id = Column(Integer, ForeignKey(User.id), index=True,
                     nullable=False)
    user = relationship(User)

    board_id = Column(Integer, ForeignKey(Board.id), index=True,
                      nullable=False)
    board = relationship(Board)

    created_at = Column(DateTime(timezone=True), nullable=False,
                        default=now(), index=True)

    def format_created_at(self, now=None):
        if now is None:
            now = datetime.datetime.now()

        if now.date() != self.created_at.date():
            return self.created_at.date().strftime('%Y.%m.%d')
        else:
            return self.created_at.time().strftime('%H:%M')

    __tablename__ = 'posts'
