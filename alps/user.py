import uuid

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.sql.functions import now
from sqlalchemy.types import Boolean, DateTime, Integer, String
from werkzeug.security import check_password_hash, generate_password_hash

from alps.db import Base

__all__ = 'User',


class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, nullable=False, unique=True)
    nickname = Column(String, index=True, nullable=False, unique=True)
    email = Column(String, index=True, nullable=False, unique=True)
    pwhash = Column(String, nullable=False)
    name = Column(String, index=True)
    description = Column(String)
    is_jbnu_student = Column(Boolean, index=True, nullable=False,
                             default=False, server_default='0')
    student_number = Column(String, index=True)
    department = Column(String, index=True)

    email_validated = Column(Boolean, nullable=False,
                             default=False, server_default='1')
    confirm_token = Column(String, index=True)

    posts = relationship('Post',
                         cascade='all, delete-orphan',
                         lazy='dynamic')

    created_at = Column(DateTime(timezone=True), nullable=False,
                        default=now())

    def set_password(self, password):
        self.pwhash = generate_password_hash(password, method='pbkdf2:sha256:2000')

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

    def is_active(self):
        return self.email_validated

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def generate_confirm_token(self):
        if not self.confirm_token:
            self.confirm_token = str(uuid.uuid4())

    __tablename__ = 'users'
