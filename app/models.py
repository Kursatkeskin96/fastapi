from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)  # Corrected spelling here
    content = Column(String, nullable=False)
    isPublished = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))