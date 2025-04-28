from sqlalchemy import Column, Integer, String, Boolean
from backend.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    username = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)  # <= toggle
    is_verified = Column(Boolean, default=False, nullable=False)
    role = Column(String, default="user")  # "user" o "admin"
    # favorites articles
    articles = relationship("Article", back_populates="user", cascade="all, delete")

