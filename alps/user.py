from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, Integer, String
from werkzeug.security import check_password_hash, generate_password_hash

from alps.db import Base

__all__ = 'User',


class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, nullable=False, unique=True)
    pwhash = Column(String, nullable=False)
    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    nickname = Column(String, index=True, nullable=False, unique=True)

    posts = relationship('Post',
                         cascade='all, delete-orphan',
                         lazy='dynamic')

    created_at = Column(DateTime(timezone=True), nullable=False,
                        default=now())

    def set_password(self, password):
        self.pwhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

    __tablename__ = 'users'
