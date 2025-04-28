from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from backend.db import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, nullable=False)
    article = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    copyright = Column(String, nullable=False)
    deleted = Column(Boolean, default=False)  # New field
    user = relationship("User", back_populates="articles")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
