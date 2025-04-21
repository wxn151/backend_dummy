from sqlalchemy import Column, Integer, String, Boolean
from backend.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    username = Column(String, nullable=True)
    # avatar = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)  # <= toggle
    # privileges
    role = Column(String, default="user")  # "user" o "admin"
