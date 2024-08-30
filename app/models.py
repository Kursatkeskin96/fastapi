from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    firstname = Column(String, nullable=False)  # Corrected spelling here
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    conference_name = Column(String, nullable=False)
    conference_detail = Column(String, nullable=False)
    conference_date = Column(String, nullable=False)
    conference_location = Column(String, nullable=False)
    status = Column(String, nullable=False, default='pending')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
